"""
comparisons.py

Compare Records to produce Comparisons.
"""
from .datatypes import Comparison, Filter, Record
from typing import Tuple, Dict, List
import pandas as pd
from dataclasses import asdict
from botech_metadata import countries as metadata
from itertools import product


def create_comparisons(
    filtered_records: List[Record],
    scenarios: Tuple[str]
) -> List[Comparison]:
    """
    Match all records, and convert them to Comparison objects.
    """
    comparisons = []
    scenario_one, scenario_two = scenarios

    df = pd.DataFrame([asdict(record) for record in filtered_records])

    for _, row in df.iterrows():
        if row['SCENARIO'] == scenario_one:
            match = df[
                (df['AUTHOR'] == row['AUTHOR'])
                & (df['COUNTRY'] == row['COUNTRY'])
                & (df['INTERVENTION'] == row['INTERVENTION'])
                & (df['SCENARIO'] == scenario_two)
            ]
            match_row = match.iloc[0]
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
                SCENARIO_ONE_EFFECTS=row['EFFECTS'],
                SCENARIO_TWO_EFFECTS=match_row['EFFECTS'],
                SCENARIO_ONE_COSTS=row['COSTS'],
                SCENARIO_TWO_COSTS=match_row['COSTS']
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
