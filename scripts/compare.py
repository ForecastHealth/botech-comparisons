"""
compare.py

Script to run the comparison API
"""
import json
import sys
import pandas as pd
from botech_comparisons import make_comparison


if __name__ == "__main__":
    fp = sys.argv[1]
    config_fp = sys.argv[2]

    df = pd.read_csv(fp, index_col=False)
    with open(config_fp, "r") as f:
        config = json.load(f)
    scenario_one, scenario_two = config["scenarios"]
    comparators = config["comparators"]
    aggregators = config["aggregators"]

    make_comparison(
        df,
        scenario_one,
        scenario_two,
        *comparators,
        **aggregators
    )
