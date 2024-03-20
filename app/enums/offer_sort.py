from enum import Enum


class OfferSortEnum(Enum):
    """
    Enumeration for sorting options for offers.
    """
    PRICE_LOWEST = 'price_lowest'
    PRICE_HIGHEST = 'price_highest'
    NEWEST = 'newest'
    OLDEST = 'oldest'
