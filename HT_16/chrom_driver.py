from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class CustomChromeDriver:
    """ A class to manage ChromeDriver with customized options. """

    USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/120.0.0.0 Safari/537.36')

    DEFAULT_SERVICE_ARGS = [
        f'--user-agent={USER_AGENT}',
        '--disable-infobars',
        '--start-maximized',
        '--hide-scrollbars'
    ]

    PREFS = {
        'excludeSwitches': ['enable-automation'],
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_settings.popups': 0,
    }

    def __init__(self):
        self.__driver = self.__init_chrom_driver()

    def __init_chrom_driver(self) -> Chrome:
        """ Initialize Chrome WebDriver with customized options. """
        chrome_options = self.__get_chrom_options()

        service = Service(executable_path=ChromeDriverManager().install())
        chrom_driver = Chrome(service=service, options=chrome_options)

        return chrom_driver

    def __get_chrom_options(self) -> ChromeOptions:
        """ Get ChromeOptions with customized preferences and arguments. """
        chrome_options = ChromeOptions()

        chrome_options.add_experimental_option('prefs', self.PREFS)

        for arg in self.DEFAULT_SERVICE_ARGS:
            chrome_options.add_argument(arg)

        return chrome_options

    def get_chrome_driver(self) -> Chrome:
        return self.__driver
