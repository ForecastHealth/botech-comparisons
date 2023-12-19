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
from .filtered_records import (
    create_filtered_records,
)
from .comparisons import (
    create_comparisons,
    create_grouped_comparisons,
)


def create_tables(
    configuration: str,
    data: pd.DataFrame
):
    """
    High level API.

    Parses a configuration file,
    generates desired elements (blueprint, filtered_records, comparisons),
    returns them as a particular format.
    """
    (
        data_type,
        data_format,
        scenarios,
        filters,
        groups,
    ) = parse_configuration(configuration)

    if data_type == "blueprint":
        blueprint = create_blueprint(data, scenarios, filters)
        return convert_elements_to_format(
            elements=blueprint,
            format=data_format,
            annotation="Blueprint"
        )
    elif data_type == "filtered_records":
        blueprint = create_blueprint(data, scenarios, filters)
        filtered_records = create_filtered_records(data, blueprint, scenarios)
        return convert_elements_to_format(
            elements=filtered_records,
            format=data_format,
            annotation="Filtered Records"
        )
    elif data_type == "comparisons":
        blueprint = create_blueprint(data, scenarios, filters)
        filtered_records = create_filtered_records(data, blueprint, scenarios)
        comparisons = create_comparisons(filtered_records, scenarios)
        grouped_comparisons = create_grouped_comparisons(comparisons, groups)
        for group in grouped_comparisons:
            for subgroup in grouped_comparisons[group]:
                annotation = f"{group} - {subgroup}"
                return convert_elements_to_format(
                    elements=grouped_comparisons[group][subgroup],
                    format=data_format,
                    annotation=annotation
                )
    else:
        raise ValueError(f"Unknown data type: {data_type}")


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
