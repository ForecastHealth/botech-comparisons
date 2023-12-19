"""
filtered_records.py

Given a blueprint, return the records which actually appear in the data source.
"""
import pandas as pd
from .datatypes import Record
from typing import List, Tuple


def _match_source_with_blueprint(
    source: pd.DataFrame,
    blueprint: List[Record]
) -> pd.DataFrame:
    """
    Match a source of data with a wish list of records.
    """
    target = pd.DataFrame(blueprint)
    condition = (
        source['AUTHOR'].isin(target['AUTHOR']) &
        source['COUNTRY'].isin(target['COUNTRY']) &
        source['INTERVENTION'].isin(target['INTERVENTION']) &
        source['SCENARIO'].isin(target['SCENARIO'])
    )
    return source[condition]


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


def create_filtered_records(
    df: pd.DataFrame,
    blueprint: List[Record],
    scenarios: Tuple[str]
) -> pd.DataFrame:
    ANNOTATION = "filtered records"
    table = _match_source_with_blueprint(df, blueprint)
    table = _remove_invalid_comparisons(table, scenarios)
    table = _remove_older_entries(table)
    records = []
    for _, row in table.iterrows():
        record = Record(
            row["AUTHOR"],
            row["COUNTRY"],
            row["INTERVENTION"],
            row["SCENARIO"],
            row["TIMESTAMP"],
            row["EFFECT"],
            row["COST"],
        )
        records.append(record)
    return ANNOTATION, table