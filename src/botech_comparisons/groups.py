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
) -> Dict[str, Dict[str, List[Union[Comparison, Record]]]]:
    """
    Group elements together based on common properties.
    """

    def get_unique_values(elements, filter_name):
        return set(getattr(elem, filter_name) for elem in elements)

    filter_to_attr = {
        Filter.AUTHOR: 'AUTHOR',
        Filter.COUNTRY: 'COUNTRY',
        Filter.INTERVENTION: 'INTERVENTION',
        Filter.REGION: 'REGION',
        Filter.INCOME: 'INCOME',
        Filter.APPENDIX_3: 'APPENDIX_3'
    }

    grouped_elements = {}
    for group in groups:
        group_key = ', '.join(filter_to_attr[f] for f in group)
        grouped_elements[group_key] = {}

        if all(isinstance(elem, Record) for elem in elements):
            unique_values = [
                get_unique_values(elements, filter_to_attr[f])
                for f in group
            ]
        elif all(isinstance(elem, Comparison) for elem in elements):
            records = [
                comp.SCENARIO_ONE
                for comp in elements
            ] + [
                comp.SCENARIO_TWO
                for comp in elements
            ]
            unique_values = [
                get_unique_values(records, filter_to_attr[f])
                for f in group
            ]
        else:
            raise ValueError("Elements must be all Comparisons or all Records")

        combinations = product(*unique_values)
        for combo in combinations:
            combo_key = ', '.join(str(item) for item in combo)
            filtered_elements = [
                elem
                for elem in elements
                if all(getattr(elem if isinstance(elem, Record) else getattr(elem, 'SCENARIO_ONE'), filter_to_attr[group[i]]) == combo[i] for i in range(len(group)))
            ]
            grouped_elements[group_key][combo_key] = filtered_elements

    return grouped_elements
