from enum import Enum


class SortCriterion(str, Enum):
    CHEAPEST = "cheapest"
    FASTEST = "fastest"
    BEST_VALUE = "best_value"
