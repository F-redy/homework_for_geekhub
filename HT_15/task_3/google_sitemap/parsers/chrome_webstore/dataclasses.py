from dataclasses import dataclass


@dataclass
class SitemapItem:
    location: str


@dataclass
class LocationItem:
    url: str


@dataclass
class LocationItemData:
    extension_id: str
    title: str
    description: str
