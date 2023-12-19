"""
wishlist.py

The methods associated with creating a wishlist.

A wishlist is a list of records that should be looked for 
in the data source. It refers to the product of every filtered
value of interest.
"""
from .datatypes import Filter, Record
import pandas as pd
from typing import Dict, List, Optional, Tuple
from botech_metadata import _records as _country_records
from botech_metadata.countries import Country
from botech_metadata import countries as metadata
from itertools import product


def _determine_filtered_values(
    df: pd.DataFrame,
    filters: Optional[Dict[Filter, List[str]]] = None
) -> Dict[Filter, List[str]]:
    get_uniques_from_df = [
        Filter.AUTHOR,
        Filter.INTERVENTION,
    ]
    filtered_values = {
        filter: []
        for filter in list(Filter)
    }
    filtered_values[Filter.COUNTRY] = _filter_countries(filters)
    for filter_type in get_uniques_from_df:
        filter_column_name = filter_type.name
        filtered_values[filter_type] = df[filter_column_name].unique().tolist()
        if filters:
            if filter_type in filters:
                filtered_values[filter_type] = filters[filter_type]
    return filtered_values


def _filter_countries(filters: Dict[Filter, List[str]]) -> List[Country]:
    "Collect all possible countries that could be included."
    all_countries = []
    country_sets = []

    # REGION filter
    regions = filters.get(Filter.REGION, [])
    if regions:
        mapping = metadata.countries_by_category("region")
        countries_by_region = {country.alpha2 for region in regions for country in mapping[region]}
        country_sets.append(countries_by_region)

    # INCOME filter
    incomes = filters.get(Filter.INCOME, [])
    if incomes:
        mapping = metadata.countries_by_category("income")
        countries_by_income = {country.alpha2 for income in incomes for country in mapping[income]}
        country_sets.append(countries_by_income)

    # APPENDIX_3 filter
    appendix_3s = filters.get(Filter.APPENDIX_3, [])
    if appendix_3s:
        mapping = metadata.countries_by_category("appendix_3")
        countries_by_appendix_3 = {country.alpha2 for appendix_3 in appendix_3s for country in mapping[appendix_3]}
        country_sets.append(countries_by_appendix_3)

    # COUNTRY filter
    if Filter.COUNTRY in filters:
        countries = set()
        for country in filters[Filter.COUNTRY]:
            try:
                countries.add(metadata.get(country).alpha2)
            except KeyError:
                pass
        country_sets.append(countries)

    # Find intersection if there are any sets to intersect
    if country_sets:
        all_countries = set.intersection(*country_sets)
    else:
        # If no filters, return all countries
        all_countries = {country.alpha2 for country in _country_records}

    return list(all_countries)


def _create_all_record_combinations(
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




def create_wish_list(
    df: pd.DataFrame,
    scenarios: Tuple[str],
    filters: Optional[Dict[Filter, List[str]]] = None
) -> List[Record]:
    """
    Create a list of records with all data requirements.
    """
    records = []
    filtered_values = _determine_filtered_values(df, filters)
    records = _create_all_record_combinations(scenarios, filtered_values)
    return records


