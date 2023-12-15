"""
datatypes.py

Defining our datastructures
"""
from enum import Enum
from dataclasses import dataclass, field
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


@dataclass
class Comparison:
    AUTHOR: str
    COUNTRY: str
    INTERVENTION: str
    SCENARIO_ONE: str
    SCENARIO_TWO: str
    TIMESTAMP: datetime.datetime
    NET_EFFECTS: float
    NET_COSTS: float
    COST_EFFECTIVENESS: float = field(init=False)

    def __post_init__(self):
        self.COST_EFFECTIVENESS = self.NET_EFFECTS / self.NET_COSTS


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
