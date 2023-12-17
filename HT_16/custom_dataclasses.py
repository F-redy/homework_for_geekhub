from dataclasses import dataclass


@dataclass
class RobotOrderData:
    order_number: str
    head: str
    body: str
    legs: str
    address: str


@dataclass
class RobotReceipt:
    id_receipt: str
    html_receipt: str
