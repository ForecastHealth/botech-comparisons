"""
datatypes.py

Defining our datastructures
"""
from botech_metadata import countries as metadata
from typing import Optional
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
    REGION: str = field(init=False)
    INCOME: str = field(init=False)
    APPENDIX_3: str = field(init=False)
    UID: Optional[str] = None

    def __post_init__(self):
        try:
            country_metadata = metadata.get(self.COUNTRY)
            self.REGION = country_metadata.region
            self.INCOME = country_metadata.income
            self.APPENDIX_3 = country_metadata.appendix_3
        except KeyError:
            self.REGION = None
            self.INCOME = None
            self.APPENDIX_3 = None


@dataclass
class Comparison:
    SCENARIO_ONE: Record
    SCENARIO_TWO: Record
    NET_EFFECTS: float = field(init=False)
    NET_COSTS: float = field(init=False)
    COST_EFFECTIVENESS: float = field(init=False)

    def __post_init__(self):
        self.NET_EFFECTS = self.SCENARIO_TWO.EFFECTS - self.SCENARIO_ONE.EFFECTS
        self.NET_COSTS = self.SCENARIO_TWO.COSTS - self.SCENARIO_ONE.COSTS

        if self.NET_COSTS != 0:
            self.COST_EFFECTIVENESS = self.NET_EFFECTS / self.NET_COSTS
        else:
            self.COST_EFFECTIVENESS = float('inf')


class Filter(Enum):
    AUTHOR = 1
    COUNTRY = 2
    INTERVENTION = 3
    REGION = 4
    INCOME = 5
    APPENDIX_3 = 6
