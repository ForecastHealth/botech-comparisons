from typing import List, Union
from .datatypes import Comparison, Record
from dataclasses import asdict
import pandas as pd


def convert_elements_to_format(
    elements: Union[List[Record], List[Comparison]],
    format: str,
    annotation: str
):
    if elements and isinstance(elements[0], Comparison):
        data = []
        for comparison in elements:
            # Create unique keys for each field in SCENARIO_ONE and SCENARIO_TWO
            s1_data = {f"S1_{k}": v for k, v in asdict(comparison.SCENARIO_ONE).items()}
            s2_data = {f"S2_{k}": v for k, v in asdict(comparison.SCENARIO_TWO).items()}

            # Merge data and add comparison specific fields
            row = {**s1_data, **s2_data,
                   'NET_EFFECTS': comparison.NET_EFFECTS,
                   'NET_COSTS': comparison.NET_COSTS,
                   'COST_EFFECTIVENESS': comparison.COST_EFFECTIVENESS}
            data.append(row)
        df = pd.DataFrame(data)
    else:
        df = pd.DataFrame([asdict(element) for element in elements])

    df.name = annotation

    # Convert DataFrame to the specified format
    if format == "dataframe":
        return df
    elif format == "csv":
        return df.to_csv(index=False)
    elif format == "html":
        return df.to_html(index=False)
    elif format == "self":
        return elements
    else:
        raise ValueError(f"Unknown format: {format}")


