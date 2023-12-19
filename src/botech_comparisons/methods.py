"""
methods.py

Methods to assist the botech-comparison API.
"""
from typing import Tuple, Dict, List, Optional
from .datatypes import Record, Filter, Comparison
import pandas as pd
from botech_metadata import _records as _country_records
from botech_metadata.countries import Country
from botech_metadata import countries as metadata
from itertools import product


def create_wish_list(
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


# TODO - This method doens't work as intended, countries
def determine_filtered_values(
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
    filtered_values[Filter.COUNTRY] = filter_countries(filters)
    for filter_type in get_uniques_from_df:
        filter_column_name = filter_type.name
        filtered_values[filter_type] = df[filter_column_name].unique().tolist()
        if filters:
            if filter_type in filters:
                filtered_values[filter_type] = filters[filter_type]
    return filtered_values


from typing import List, Dict
from collections import Counter

def filter_countries(filters: Dict[Filter, List[str]]) -> List[Country]:
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


def create_realistic_table(
    df: pd.DataFrame,
    wish_list: List[Record],
    scenarios: Tuple[str]
) -> pd.DataFrame:
    """
    Create a list of records with all data requirements.
    """
    table = match_source_with_wish_list(df, wish_list)
    table = remove_invalid_comparisons(table, scenarios)
    table = remove_older_entries(table)
    return table


def match_source_with_wish_list(
    source: pd.DataFrame,
    wish_list: List[Record]
) -> pd.DataFrame:
    """
    Match a source of data with a wish list of records.
    """
    target = pd.DataFrame(wish_list)
    condition = (
        source['AUTHOR'].isin(target['AUTHOR']) &
        source['COUNTRY'].isin(target['COUNTRY']) &
        source['INTERVENTION'].isin(target['INTERVENTION']) &
        source['SCENARIO'].isin(target['SCENARIO'])
    )
    return source[condition]


def remove_invalid_comparisons(df: pd.DataFrame, scenarios: Tuple[str]):
    """
    For each AUTHOR, COUNTRY, INTERVENTION,
    if both scenarios are not present, remove those rows.
    Keep only the most recent entry for each scenario.
    """
    scenario_one, scenario_two = scenarios
    df = df.groupby(['AUTHOR', 'COUNTRY', 'INTERVENTION'])
    df = df.filter(lambda x: (x['SCENARIO'] == scenario_one).any() and (x['SCENARIO'] == scenario_two).any())
    return df


def remove_older_entries(df: pd.DataFrame):
    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"])
    df = df.groupby(['AUTHOR', 'COUNTRY', 'INTERVENTION', 'SCENARIO'])
    df = df.apply(lambda x: x.nlargest(1, 'TIMESTAMP'))
    df = df.reset_index(drop=True)
    return df


def make_comparisons(df, scenarios: Tuple[str]) -> List[Comparison]:
    """
    Match all records, and convert them to Comparison objects.
    """
    comparisons = []
    scenario_one, scenario_two = scenarios

    for _, row in df.iterrows():
        if row['SCENARIO'] == scenario_one:
            match = df[(df['AUTHOR'] == row['AUTHOR']) & (df['COUNTRY'] == row['COUNTRY']) & 
                       (df['INTERVENTION'] == row['INTERVENTION']) & (df['SCENARIO'] == scenario_two)]

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


def group_comparisons(
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


def convert_comparisons_to_tables(
    grouped_comparisons: List[List[Comparison]]
) -> List[pd.DataFrame]:
    ...

