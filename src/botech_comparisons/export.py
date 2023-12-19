import pandas as pd
from typing import Dict, Tuple, List, Union
from .data import Comparison, Record


def convert_comparisons_to_tables(
    grouped_comparisons: Dict[str, Dict[str, List[Comparison]]]
) -> List[Tuple[str, pd.DataFrame]]:
    tables = []
    for broad_group_label in grouped_comparisons:
        for specific_group_label in grouped_comparisons[broad_group_label]:
            table = pd.DataFrame([asdict(comp) for comp in grouped_comparisons[broad_group_label][specific_group_label]])
            tables.append((broad_group_label, specific_group_label, table))
    return tables


def convert_objects_to_format(
    obj: List[Union[Comparison, Record]],
    format: str
):
    ...
