"""
main.py

Run the main API
"""
from src.botech_comparisons import create_tables
import sys
import json
import pandas as pd
import pprint


def main():
    configuration_filepath = sys.argv[1]
    mock_data_filepath = sys.argv[2]
    data_type = sys.argv[3]
    data_format = sys.argv[4]

    with open(configuration_filepath) as f:
        configuration = json.load(f)
    configuration["data_type"] = data_type
    configuration["data_format"] = data_format

    df = pd.read_csv(mock_data_filepath, keep_default_na=False)

    foo = create_tables(configuration, df)
    pprint.pprint(foo)


if __name__ == "__main__":
    main()
