"""
methods.py

Methods to assist the botech-comparison API.
"""
from typing import Tuple, Dict, List, Optional
from .datatypes import Record, Filter, Group
import pandas as pd
from botech_metadata import _records as _country_records
from botech_metadata.countries import Country
from botech_metadata import countries as metadata
from itertools import product


def generate_wish_list(
    df: pd.DataFrame,
    scenarios: Tuple[str],
    filters: Optional[Dict[Filter, List[str]]] = None
) -> List[Record]:
    """
    Create a list of records with all data requirements.
    """
    records = []
    filtered_values = determine_filtered_values(df, filters)
    records = create_all_record_combinations(scenarios, filtered_values)
    return records


def determine_filtered_values(
    df: pd.DataFrame,
    filters: Optional[Dict[Filter, List[str]]] = None
) -> Dict[Filter, List[str]]:
    get_uniques_from_df = [
        Filter.AUTHOR,
        Filter.INTERVENTION,
    ]
    get_uniques_from_metadata = [
        Filter.REGION,
        Filter.INCOME,
        Filter.APPENDIX_3,
    ]
    filtered_values = {
        filter: []
        for filter in list(Filter)
    }
    filtered_values[Filter.COUNTRY] = filter_countries(filters)
    for filter_type in get_uniques_from_df:
        filter_column_name = filter_type.name
        filtered_values[filter_type] = df[filter_column_name].unique().tolist()
        if filters:
            if filter_type in filters:
                filtered_values[filter_type] = filters[filter_type]
    for filter_type in get_uniques_from_metadata:
        filter_column_name = filter_type.name
        filtered_values[filter_type] = list(
            metadata.countries_by_category(filter_column_name).keys()
        )
        if filters:
            if filter_type in filters:
                filtered_values[filter_type] = filters[filter_type]
    return filtered_values


def filter_countries(filters: Dict[Filter, List[str]]) -> List[Country]:
    "Collect all possible countries that could be included."
    countries = _country_records
    if filters:
        if Filter.COUNTRY in filters:
            countries = [
                metadata.get(country).alpha3
                for country in filters[Filter.COUNTRY]
            ]
    return countries


def create_all_record_combinations(
    scenarios: Tuple[str],
    filtered_values: Dict[Filter, List[str]],
) -> List[Record]:
    """
    Make all possible combinations of records.
    """
    records = []
    authors = filtered_values.get(Filter.AUTHOR, [None])
    countries = filtered_values.get(Filter.COUNTRY, [None])
    interventions = filtered_values.get(Filter.INTERVENTION, [None])
    scenarios = list(scenarios)
    timestamps = [None]
    effects = [None]
    costs = [None]

    for combination in product(
        authors,
        countries,
        interventions,
        scenarios,
        timestamps,
        effects,
        costs
    ):
        record = Record(*combination)
        records.append(record)

    return records
