"""
botech_comparisons.py

Compare model runs from arbitrary lists of summarised results.
"""
import pandas as pd
from typing import Tuple, List, Optional
from .datatypes import Filter
from .export import convert_objects_to_format
from .wishlist import create_wish_list
from .filtered_records import create_filtered_records
from .comparisons import create_comparisons, create_grouped_comparisons


def create_tables(
    configuration_filepath: str,
    data_filepath: str
):
    """
    High level API - handles unpacking, parsing etc.
    """
    (
        data_type,
        data_format,
        scenarios,
        filters,
        groups,
    ) = parse_configuration(configuration_filepath)
    data = pd.read_csv(data_filepath)

    if data_type == "wishlist":
        wish_list = create_wish_list(data, scenarios, filters)
        return convert_objects_to_format(wish_list, format)
    elif data_type == "filtered_records":
        wish_list = create_wish_list(data, scenarios, filters)
        filtered_records = create_filtered_records(data, wish_list, scenarios)
        return convert_objects_to_format(filtered_records, format)
    elif data_type == "comparisons":
        wish_list = create_wish_list(data, scenarios, filters)
        filtered_records = create_filtered_records(data, wish_list, scenarios)
        comparisons = create_comparisons(filtered_records, scenarios)
        grouped_comparisons = create_grouped_comparisons(comparisons, groups)
        return convert_objects_to_format(grouped_comparisons, format)
    else:
        raise ValueError(f"Unknown data type: {data_type}")


def parse_configuration(
    configuration: dict
) -> Tuple[List[str], str, tuple, Optional[dict], Optional[list]]:
    """
    Given a configuration, return the appropriate data structures.
    """
    data_type = configuration["data_type"],
    data_format = configuration["data_format"],
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
    return data_type, data_format, scenarios, filters, groups


__all__ = [
    "create_tables",
    "parse_configuration"
]
