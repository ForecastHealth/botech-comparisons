"""
botech_comparisons.py

Compare model runs from arbitrary lists of summarised results.
"""
import pandas as pd
from typing import Tuple, List, Optional
from .datatypes import Filter
from .convert import (
    convert_elements_to_format,
)
from .blueprint import (
    create_blueprint,
)
from .records import (
    create_records,
    filter_records
)
from .comparisons import (
    create_comparisons,
)
from .groups import (
    group_elements
)


def create_tables(
    configuration: dict,
    data: pd.DataFrame
):
    """
    High level API.

    Parses a configuration file,
    generates desired elements: records, comparisons
    returns them as a particular format.
    """
    (
        data_type,
        data_format,
        scenarios,
        filters,
        groups,
    ) = parse_configuration(configuration)

    records = create_records(data)
    filtered_records = filter_records(records, scenarios, filters)
    if not filtered_records:
        raise ValueError("No records matched the filters provided.")

    if data_type == "records":
        elements = filtered_records

    elif data_type == "comparisons":
        comparisons = create_comparisons(records, scenarios)
        elements = comparisons
    else:
        raise ValueError(f"Unknown data type: {data_type}")

    # if groups:
    #     grouped_elements = group_elements(groups, elements)
    return convert_elements_to_format(
        elements=elements,
        format=data_format,
        annotation=data_format
        )


def parse_configuration(
    configuration: dict
) -> Tuple[List[str], str, tuple, Optional[dict], Optional[list]]:
    """
    Given a configuration, return the appropriate data structures.
    """
    data_type = configuration["data_type"]
    data_format = configuration["data_format"]
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
