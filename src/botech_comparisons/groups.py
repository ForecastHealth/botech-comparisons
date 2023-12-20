"""
groups.py

Methods to group elements together,
based on common properties e.g. region, income.
"""
from .datatypes import Comparison, Filter, Record
from typing import Dict, List, Union
from itertools import product


def group_elements(
    groups: List[List[Filter]],
    elements: List[Union[Comparison, Record]]
):
    """
    Group elements together based on common properties.
    """
    ...


def create_grouped_comparisons(
    comparisons: List[Comparison],
    groups: List[List[Filter]]
) -> Dict[str, Dict[str, List[Comparison]]]:

    def get_unique_values(comparisons, filter_name):
        return set(getattr(comp, filter_name) for comp in comparisons)

    filter_to_attr = {
        Filter.AUTHOR: 'AUTHOR',
        Filter.COUNTRY: 'COUNTRY',
        Filter.INTERVENTION: 'INTERVENTION',
        Filter.REGION: 'REGION',
        Filter.INCOME: 'INCOME',
        Filter.APPENDIX_3: 'APPENDIX_3'
    }

    grouped_comparisons = {}
    for group in groups:
        group_key = ', '.join(filter_to_attr[f] for f in group)
        grouped_comparisons[group_key] = {}
        unique_values = [get_unique_values(comparisons, filter_to_attr[f]) for f in group]
        combinations = product(*unique_values)
        for combo in combinations:
            combo_key = ', '.join(str(item) for item in combo)
            filtered_comps = [
                comp
                for comp in comparisons
                if all(getattr(comp, filter_to_attr[group[i]]) == combo[i] for i in range(len(group)))
            ]
            grouped_comparisons[group_key][combo_key] = filtered_comps
    return grouped_comparisons
