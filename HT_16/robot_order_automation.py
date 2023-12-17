import os
import shutil
from dataclasses import astuple
from io import BytesIO
from pathlib import Path
from random import randrange
from urllib.parse import urljoin

from PIL import Image
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from xhtml2pdf import pisa

from HT_16.chrom_driver import CustomChromeDriver
from HT_16.custom_dataclasses import RobotReceipt
from HT_16.csv_order_reader import CSVOrderReader


class RobotOrderAutomation:
    """
    Automates the process of ordering robots from 'https://robotsparebinindustries.com/'.

    This class manages the automation of ordering robots by performing actions such as selecting parts,
    filling in details, take screenshot of the robot, generating receipts, and saving them as PDF files.
    """

    TIMEOUT_ACTION = 1
    TIMEOUT_FOR_ELEM = 5
    MAIN_URL = 'https://robotsparebinindustries.com/'
    CSV_FIVE = urljoin(MAIN_URL, 'orders.csv')
    PATH_TO_SAVE = Path(os.getcwd(), 'output')

    def __init__(self):
        self.__driver = CustomChromeDriver().get_chrome_driver()
        self.__image = None
        self.__screenshot = None

    def start(self) -> None:
        """
        Initiates the order processing routine.

        It prepares the output folder, reads orders from the CSV file, and navigates to the main page.
        It processes each order by selecting robot parts, filling in details, and generating receipts.
        Once all orders are processed, it closes the driver session.
        """

        self.__prepare_output_folder()
        orders = CSVOrderReader(self.CSV_FIVE).read_order_file()
        self.__open_main_page()

        total_orders_processed = 0

        try:
            self.__go_to_order_page()
            for order in orders:
                order_number, head, body, legs, address = astuple(order)
                self.__order_robot(head, body, legs, address)
                total_orders_processed += 1
                print(f'Order number {order_number} - processed!')

        except Exception as e:
            print(e)
        else:
            print(f'\nTotal orders processed: {total_orders_processed}.')
        finally:
            self.__driver.close()
            self.__driver.quit()

    def __order_robot(self, head: str, body: str, legs: str, address: str) -> None:
        """
        Completes the process of ordering a robot.

        It executes a series of actions: closes any popups, selects the robot head and body, inputs the number of legs
        and shipping address, clicks the preview button to generate the robot preview, scrolls to the robot image,
        takes a screenshot, proceeds to place the order, saves the receipt as a PDF,
        and finally clicks to start ordering another robot.

        :param head: The choice for the robot's head.
        :param body: The choice for the robot's body.
        :param legs: The number of legs for the robot.
        :param address: The shipping address for the order.
        """
        self.__close_popup()
        self.__choose_head(head)
        self.__choose_body(body)
        self.__input_legs(legs)
        self.__input_address(address)
        self.__click_preview_button()
        self.__scroll_to_image()
        self.__take_screenshot()
        self.__click_order_button()
        self.__save_receipt_to_pdf()
        self.__click_another_order()

    def __prepare_output_folder(self) -> None:
        """
        Prepares the output folder for saving files.

        If the output folder exists, it removes all its contents. Otherwise, it creates a new directory to save files.
        """
        if self.PATH_TO_SAVE.is_dir():
            shutil.rmtree(self.PATH_TO_SAVE)
        self.PATH_TO_SAVE.mkdir(parents=True, exist_ok=True)

    def __click_element_with_js(self, element) -> None:
        """
            Clicks on a web element using JavaScript.

            Args:
                element: The web element to be clicked.

            Note:
                This method triggers a click event on the specified web element using JavaScript.
        """
        self.__driver.execute_script('arguments[0].click();', element)

    def __wait_for_element(self, by: str, selector: str, timeout: int = TIMEOUT_FOR_ELEM) -> None:
        """
        Waits for the specified web element to become clickable and performs a JavaScript click action.

        Args:
            by (str): The method of locating the element (e.g., By.ID, By.CSS_SELECTOR, etc.).
            selector (str): The selector pattern to find the element.
            timeout (int, optional): The maximum time in seconds to wait for the element to become clickable.
                                     Defaults to TIMEOUT_FOR_ELEM.

        Note:
            This method waits for the element specified by 'by' and 'selector' to be clickable and then performs
            a JavaScript click action on it.
        """
        self.__wait_until()
        wait = WebDriverWait(self.__driver, timeout)
        element = wait.until(expected_conditions.element_to_be_clickable((by, selector)))

        self.__click_element_with_js(element)

    def __wait_until(self, timeout: int = TIMEOUT_ACTION) -> None:
        """
            Pauses the execution for a random interval within the specified timeout duration.

            Args:
                timeout (int, optional): The maximum time in seconds to wait before performing the next action.
                                         Defaults to TIMEOUT_ACTION.

            Note:
                This method uses a randomized pause within the timeout duration to simulate human-like delays.
        """
        action = ActionChains(self.__driver)
        action.pause(randrange(timeout, timeout + 2, 1))
        action.perform()

    def __open_main_page(self) -> None:
        self.__driver.get(self.MAIN_URL)

    def __go_to_order_page(self) -> None:
        self.__wait_for_element(By.LINK_TEXT, 'Order your robot!')

    def __close_popup(self) -> None:
        """ Closes the popup window on the page. """

        self.__wait_until()
        self.__wait_for_element(By.CSS_SELECTOR, 'button.btn-dark')

    def __choose_head(self, head_option) -> None:
        self.__wait_until()
        head_elem = Select(self.__driver.find_element(By.CSS_SELECTOR, '#head.custom-select'))
        head_elem.select_by_index(head_option)

    def __choose_body(self, body_option) -> None:
        self.__wait_until()
        self.__wait_for_element(By.CSS_SELECTOR, f'#id-body-{body_option}.form-check-input')

    def __input_legs(self, number_legs) -> None:
        self.__wait_until()
        legs_input = self.__driver.find_element(By.CSS_SELECTOR, 'input[type="number"]')
        legs_input.send_keys(number_legs)

    def __input_address(self, shipping_address) -> None:
        self.__wait_until()
        address = self.__driver.find_element(By.ID, 'address')
        address.send_keys(shipping_address)

    def __click_preview_button(self) -> None:
        self.__wait_for_element(By.ID, 'preview')

    def __scroll_to_image(self) -> None:
        """ Scrolls the page to bring the robot image into view. """

        self.__wait_until()
        self.__image = self.__driver.find_element(By.CSS_SELECTOR, '#robot-preview-image')
        self.__driver.execute_script('arguments[0].scrollIntoView(true);', self.__image)

    def __take_screenshot(self) -> None:
        self.__wait_until()
        self.__screenshot = Image.open(BytesIO(self.__image.screenshot_as_png))

    def __click_order_button(self) -> None:

        while True:
            try:
                self.__wait_for_element(By.ID, 'order')
                self.__driver.find_element(By.ID, 'order-completion')

                return
            except NoSuchElementException:
                self.__wait_until()
                continue

    @staticmethod
    def __get_id_receipt(receipt_element) -> str:
        robo_order = receipt_element.find_element(By.CLASS_NAME, 'badge-success')
        return robo_order.text.split('-')[-1]

    def __get_receipt(self) -> RobotReceipt:
        """ Retrieving the id_receipt and html code receipt from receipt. """

        receipt_element = self.__driver.find_element(By.CSS_SELECTOR, '#receipt.alert.alert-success')

        id_receipt = self.__get_id_receipt(receipt_element)
        html_receipt = receipt_element.get_attribute('innerHTML')

        return RobotReceipt(id_receipt=id_receipt, html_receipt=html_receipt)

    def __save_receipt_to_pdf(self) -> None:
        """
            Saves the receipt information as a PDF file.

            This method generates a PDF receipt with the provided HTML content and a screenshot of the robot.

            Raises:
                FileNotFoundError: If the file is not found during the saving process.
                PermissionError: If there's a permission issue while saving the PDF.
                RuntimeError: If a runtime error occurs during the PDF creation.
                IOError: If an I/O error occurs during the file handling.
                Exception: For any other unspecified error during the receipt saving process.
        """
        receipt = self.__get_receipt()

        try:
            image = str(self.PATH_TO_SAVE / f'{receipt.id_receipt}_robot.png')
            pdf = f'{str(self.PATH_TO_SAVE / receipt.id_receipt)}_robot.pdf'

            self.__screenshot.save(image, format='PNG')

            content = f'{receipt.html_receipt}'
            content += f'<img src="{image}"/>'

            with open(pdf, 'w+b') as pdf_file:
                pisa.CreatePDF(content, pdf_file)

            # Удаление временного файла изображения
            if os.path.exists(image):
                os.remove(image)

        except FileNotFoundError as e:
            print(f'File not found: {e}')
        except PermissionError as e:
            print(f'Permission denied: {e}')
        except RuntimeError as e:
            print(f'Runtime error occurred: {e}')
        except IOError as e:
            print(f'IOError occurred: {e}')
        except Exception as e:
            print(f'Error saving receipt: {e}')

    def __click_another_order(self) -> None:
        self.__driver.find_element(By.ID, 'order-another').click()


if __name__ == '__main__':
    robot = RobotOrderAutomation()
    robot.start()
