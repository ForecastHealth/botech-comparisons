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
    REGION: str
    INCOME: str
    APPENDIX_3: bool
    INTERVENTION: str
    SCENARIO_ONE: str
    SCENARIO_TWO: str
    SCENARIO_ONE_EFFECTS: float
    SCENARIO_TWO_EFFECTS: float
    SCENARIO_ONE_COSTS: float
    SCENARIO_TWO_COSTS: float
    NET_EFFECTS: float = field(init=False)
    NET_COSTS: float = field(init=False)
    COST_EFFECTIVENESS: float = field(init=False)

    def __post_init__(self):
        self.NET_EFFECTS = self.SCENARIO_TWO_EFFECTS - self.SCENARIO_ONE_EFFECTS
        self.NET_COSTS = self.SCENARIO_TWO_COSTS - self.SCENARIO_ONE_COSTS
        self.COST_EFFECTIVENESS = self.NET_EFFECTS / self.NET_COSTS


class Filter(Enum):
    AUTHOR = 1
    COUNTRY = 2
    INTERVENTION = 3
    REGION = 4
    INCOME = 5
    APPENDIX_3 = 6
