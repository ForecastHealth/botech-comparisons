"""
botech_comparisons.py

Compare model runs from arbitrary lists of summarised results.
"""
import pandas as pd
from typing import Dict, Tuple, List, Optional
from .methods import (
    create_wish_list,
    create_realistic_table
)
from .datatypes import Filter, Group


def create_tables(
    data: pd.DataFrame,
    scenarios: Tuple[str],
    filters: Optional[Dict[Filter, List[str]]] = None,
    groupings: Optional[List[Group]] = None
):
    """
    Produce a list of tables (dataframes) of compared results.
    """
    wish_list = create_wish_list(data, scenarios, filters)
    table = create_realistic_table(data, wish_list, scenarios)
    return table
    # table = make_comparisons(table)
    # tables = group_tables(table, groupings)
    # return tables


def parse_configuration(
    configuration: dict
) -> Tuple[tuple, Optional[dict], Optional[dict]]:
    """
    Given a configuration, return the appropriate data structures.
    """
    scenarios = tuple(configuration["scenarios"])
    if "filters" in configuration:
        filters = {
            Filter[filter.upper()]: values
            for filter, values in configuration["filters"].items()
        }
    else:
        filters = None

    if "groups" in configuration:
        groups = {
            Group[group.upper()]: values
            for group, values in configuration["groups"].items()
        }
    else:
        groups = None
    return scenarios, filters, groups


__all__ = [
    "create_tables",
    "parse_configuration"
]
