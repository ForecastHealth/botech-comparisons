"""
table.py

Create a table of hypothetical records.
"""
from src.botech_comparisons import parse_configuration, create_tables
import pandas as pd
import json


def main():
    configuration_filepath = "./tests/configuration.json"
    data = pd.read_csv("./tests/MOCK_DATA.csv")
    with open(configuration_filepath, "r") as f:
        configuration = json.load(f)
    scenarios, filters, _ = parse_configuration(configuration)
    df = create_tables(data, scenarios, filters)
    print(len(df.index))
    print(df.head())


if __name__ == "__main__":
    main()
