"""
table.py

Create a table of hypothetical records.
"""
from src.botech_comparisons import (
    create_tables,
    parse_configuration,
)
import pandas as pd
import json


def main():
    configuration_filepath = "./tests/configuration.json"
    data = pd.read_csv("./tests/MOCK_DATA.csv")
    with open(configuration_filepath, "r") as f:
        configuration = json.load(f)
    scenarios, filters, groups = parse_configuration(configuration)
    records = create_tables(data, scenarios, filters)
    df = pd.DataFrame(records)
    print(len(df.index))
    print(df.head())



if __name__ == "__main__":
    main()
