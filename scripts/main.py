"""
main.py

Run the main API
"""
from src.botech_comparisons import parse_configuration, create_tables
import pandas as pd
import json
import pprint


def main():
    configuration_filepath = "./tests/configuration.json"
    data = pd.read_csv("./tests/MOCK_DATA.csv")
    with open(configuration_filepath, "r") as f:
        configuration = json.load(f)
    scenarios, filters, groups = parse_configuration(configuration)
    foo = create_tables(data, scenarios, filters, groups)
    pprint.pprint(foo)


if __name__ == "__main__":
    main()
