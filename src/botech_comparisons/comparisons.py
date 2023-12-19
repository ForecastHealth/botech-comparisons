"""
comparisons.py

Compare Records to produce Comparisons.
"""
from .data_types import Comparison, Filter
from typing import Tuple, Dict, List
import pandas as pd
from botech_metadata import countries as metadata
from itertools import product


def create_comparisons(
    filtered_records: pd.DataFrame,
    scenarios: Tuple[str]
) -> List[Comparison]:
    """
    Match all records, and convert them to Comparison objects.
    """
    comparisons = []
    scenario_one, scenario_two = scenarios

    for _, row in filtered_records.iterrows():
        if row['SCENARIO'] == scenario_one:
            match = filtered_records[
                (filtered_records['AUTHOR'] == row['AUTHOR'])
                & (filtered_records['COUNTRY'] == row['COUNTRY'])
                & (filtered_records['INTERVENTION'] == row['INTERVENTION'])
                & (filtered_records['SCENARIO'] == scenario_two)
            ]
            match_row = match.iloc[0]
            net_effects = match_row['EFFECTS'] - row['EFFECTS']
            net_costs = match_row['COSTS'] - row['COSTS']
            country = row["COUNTRY"]
            country_object = metadata.get(country)
            region = country_object.region
            income = country_object.income
            appendix_3 = country_object.appendix_3
            comparison = Comparison(
                AUTHOR=row['AUTHOR'],
                COUNTRY=country,
                REGION=region,
                INCOME=income,
                APPENDIX_3=appendix_3,
                INTERVENTION=row['INTERVENTION'],
                SCENARIO_ONE=str(scenario_one),
                SCENARIO_TWO=str(scenario_two),
                NET_EFFECTS=net_effects,
                NET_COSTS=net_costs
            )
            comparisons.append(comparison)

    return comparisons


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
