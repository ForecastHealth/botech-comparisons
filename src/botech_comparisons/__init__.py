"""
botech_comparisons.py

Compare model runs from arbitrary lists of summarised results.
"""
import pandas as pd
from typing import Dict, Tuple, List, Optional
from .methods import (
    create_wish_list,
    create_realistic_table,
    make_comparisons,
    group_comparisons,
    convert_comparisons_to_tables
)
from .datatypes import Filter


def create_tables(
    data: pd.DataFrame,
    scenarios: Tuple[str],
    filters: Optional[Dict[Filter, List[str]]] = None,
    groups: Optional[List[List[Filter]]] = None
):
    """
    Produce a list of tables (dataframes) of compared results.
    """
    wish_list = create_wish_list(data, scenarios, filters)
    table = create_realistic_table(data, wish_list, scenarios)
    comparisons = make_comparisons(table, scenarios)
    if groups:
        grouped_comparisons = group_comparisons(comparisons, groups)
        tables = convert_comparisons_to_tables(grouped_comparisons)
    else:
        tables = convert_comparisons_to_tables([comparisons])
    return tables


def parse_configuration(
    configuration: dict
) -> Tuple[tuple, Optional[dict], Optional[list]]:
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
        groups = [
            [Filter[group.upper()] for group in arrangement]
            for arrangement in configuration["groups"]
        ]
    else:
        groups = None
    return scenarios, filters, groups


__all__ = [
    "create_tables",
    "parse_configuration"
]
