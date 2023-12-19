from typing import List, Union
from .data import Comparison, Record
from dataclasses import asdict
import pandas as pd


def convert_elements_to_format(
    elements: Union[List[Record], List[Comparison]],
    format: str,
    annotation: str
):
    """
    Convert a list of Records or Comparisons.

    Parameters:
    -----------
    elements: List[Record] or List[Comparison]
        A list of Records or Comparisons.
    format: str
        The format to convert the elements to.
        Either "csv" or "html"
    annotation: str
        The annotation to (possibly) add to the table.
    """
    df = pd.DataFrame([asdict(element) for element in elements])
    df.name = annotation
    if format == "csv":
        return df.to_csv(index=False)
    elif format == "html":
        return df.to_html(index=False)
    else:
        raise ValueError(f"Unknown format: {format}")