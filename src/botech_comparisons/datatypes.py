"""
datatypes.py

Defining our datastructures
"""
from enum import Enum
from dataclasses import dataclass
import datetime


@dataclass
class Record:
    AUTHOR: str
    COUNTRY: str
    INTERVENTION: str
    SCENARIO: str
    TIMESTAMP: datetime.datetime
    EFFECTS: float
    COSTS: float


class Group(Enum):
    REGION = 1
    INCOME = 2
    APPENDIX_3 = 3


class Filter(Enum):
    AUTHOR = 1
    COUNTRY = 2
    INTERVENTION = 3
    REGION = 4
    INCOME = 5
    APPENDIX_3 = 6
