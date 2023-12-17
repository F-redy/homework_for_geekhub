import csv
from io import StringIO

import requests

from HT_16.custom_dataclasses import RobotOrderData


class CSVOrderReader:
    def __init__(self, url: str):
        self.orders_url = url

    def read_order_file(self) -> list[RobotOrderData] | None:
        """Reads data from the order file.

        Fetches the CSV data from the specified URL and reads it into a list of dictionaries.

        Returns:
            list[dict] | None: A list of dictionaries representing the CSV data if successful, otherwise None.
        """
        response = requests.get(self.orders_url)
        response.raise_for_status()
        csv_data = csv.reader(StringIO(response.text))

        return [RobotOrderData(*row) for row in list(csv_data)[1:]]
