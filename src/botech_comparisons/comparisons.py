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
    scenario_one_label, scenario_two_label = scenarios

    df = pd.DataFrame([asdict(record) for record in filtered_records])

    for _, row in df.iterrows():
        if row['SCENARIO'] == scenario_one_label:
            match = df[
                (df['AUTHOR'] == row['AUTHOR'])
                & (df['COUNTRY'] == row['COUNTRY'])
                & (df['INTERVENTION'] == row['INTERVENTION'])
                & (df['SCENARIO'] == scenario_two_label)
            ]
            if not match.empty:
                match_row = match.iloc[0]

                # Create Record instances for each scenario
                scenario_one_record = Record(
                    UID=row.get('UID'),
                    AUTHOR=row['AUTHOR'],
                    COUNTRY=row['COUNTRY'],
                    INTERVENTION=row['INTERVENTION'],
                    SCENARIO=row['SCENARIO'],
                    TIMESTAMP=row['TIMESTAMP'],
                    EFFECTS=row['EFFECTS'],
                    COSTS=row['COSTS']
                )

                scenario_two_record = Record(
                    UID=match_row.get('UID'),
                    AUTHOR=match_row['AUTHOR'],
                    COUNTRY=match_row['COUNTRY'],
                    INTERVENTION=match_row['INTERVENTION'],
                    SCENARIO=match_row['SCENARIO'],
                    TIMESTAMP=match_row['TIMESTAMP'],
                    EFFECTS=match_row['EFFECTS'],
                    COSTS=match_row['COSTS']
                )

                # Create a Comparison object
                comparison = Comparison(
                    SCENARIO_ONE=scenario_one_record,
                    SCENARIO_TWO=scenario_two_record
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
