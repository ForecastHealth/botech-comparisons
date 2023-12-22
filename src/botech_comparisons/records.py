"""
records.py

Given a blueprint, return the records which actually appear in the data source.
"""
import pandas as pd
from .datatypes import Record, Filter
from typing import List, Tuple, Dict, Optional


def create_records(df: pd.DataFrame) -> List[Record]:
    records = []
    for _, row in df.iterrows():
        uid = row.get("UID", None)
        record = Record(
            UID=uid,
            AUTHOR=row["AUTHOR"],
            COUNTRY=row["COUNTRY"],
            INTERVENTION=row["INTERVENTION"],
            SCENARIO=row["SCENARIO"],
            TIMESTAMP=row["TIMESTAMP"],
            EFFECTS=row["EFFECTS"],
            COSTS=row["COSTS"],
        )
        records.append(record)
    return records


def _remove_invalid_comparisons(df: pd.DataFrame, scenarios: Tuple[str]):
    """
    For each AUTHOR, COUNTRY, INTERVENTION,
    if both scenarios are not present, remove those rows.
    Keep only the most recent entry for each scenario.
    """
    scenario_one, scenario_two = scenarios
    df = df.groupby(['AUTHOR', 'COUNTRY', 'INTERVENTION'])
    df = df.filter(lambda x: (x['SCENARIO'] == scenario_one).any() and (x['SCENARIO'] == scenario_two).any())
    return df


def _remove_older_entries(df: pd.DataFrame):
    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"])
    df = df.groupby(['AUTHOR', 'COUNTRY', 'INTERVENTION', 'SCENARIO'])
    df = df.apply(lambda x: x.nlargest(1, 'TIMESTAMP'))
    df = df.reset_index(drop=True)
    return df


def filter_records(
    records: List[Record],
    scenarios: Tuple[str],
    filters: Optional[Dict[Filter, List[str]]] = None
) -> List[Record]:
    filtered_records = []
    for record in records:
        if record.SCENARIO not in scenarios:
            continue

        match = True
        if filters:
            for filter_type, values in filters.items():
                record_value = getattr(record, filter_type.name)
                if record_value not in values:
                    match = False
                    break

        if match:
            filtered_records.append(record)

    return filtered_records
