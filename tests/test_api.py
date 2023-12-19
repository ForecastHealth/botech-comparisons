import warnings
import json
import pandas as pd
import unittest
from src.botech_comparisons import create_tables
warnings.filterwarnings("ignore")


class TestBluePrint(unittest.TestCase):
    def load_configuration(self, filepath: str, **kwargs) -> dict:
        with open(filepath, "r") as f:
            configuration = json.load(f)
        for key, value in kwargs.items():
            configuration[key] = value
        return configuration

    def setUp(self):
        self.configuration_sml = "./tests/minimal_configuration.json"
        self.configuration_med = "./tests/configuration.json"
        self.configuration_lrg = "./tests/full_configuration.json"
        self.mock_data = pd.read_csv("./tests/MOCK_DATA.csv")

    def test_self(self):
        kwargs = {
            "data_type": "blueprint",
            "data_format": "self"
        }

        configuration = self.load_configuration(self.configuration_sml, **kwargs)
        foo = create_tables(
            configuration=configuration,
            data=self.mock_data
        )
        self.assertIsInstance(foo, list)

        configuration = self.load_configuration(self.configuration_med, **kwargs)
        bar = create_tables(
            configuration=configuration,
            data=self.mock_data
        )
        self.assertIsInstance(bar, list)

        configuration = self.load_configuration(self.configuration_lrg, **kwargs)
        baz = create_tables(
            configuration=configuration,
            data=self.mock_data
        )
        self.assertIsInstance(baz, list)

    def test_csv(self):
        kwargs = {
            "data_type": "blueprint",
            "data_format": "csv"
        }

        configuration = self.load_configuration(self.configuration_sml, **kwargs)
        foo = create_tables(
            configuration=configuration,
            data=self.mock_data
        )
        self.assertIsInstance(foo, str)

        configuration = self.load_configuration(self.configuration_med, **kwargs)
        bar = create_tables(
            configuration=configuration,
            data=self.mock_data
        )
        self.assertIsInstance(bar, str)

        configuration = self.load_configuration(self.configuration_lrg, **kwargs)
        baz = create_tables(
            configuration=configuration,
            data=self.mock_data
        )
        self.assertIsInstance(baz, str)

    def test_html(self):
        kwargs = {
            "data_type": "blueprint",
            "data_format": "html"
        }

        configuration = self.load_configuration(self.configuration_sml, **kwargs)
        foo = create_tables(
            configuration=configuration,
            data=self.mock_data
        )
        self.assertIsInstance(foo, str)

        configuration = self.load_configuration(self.configuration_med, **kwargs)
        bar = create_tables(
            configuration=configuration,
            data=self.mock_data
        )
        self.assertIsInstance(bar, str)

        configuration = self.load_configuration(self.configuration_lrg, **kwargs)
        baz = create_tables(
            configuration=configuration,
            data=self.mock_data
        )
        self.assertIsInstance(baz, str)

    def test_df(self):
        kwargs = {
            "data_type": "blueprint",
            "data_format": "dataframe"
        }

        configuration = self.load_configuration(self.configuration_sml, **kwargs)
        foo = create_tables(
            configuration=configuration,
            data=self.mock_data
        )
        self.assertIsInstance(foo, pd.DataFrame)

        configuration = self.load_configuration(self.configuration_med, **kwargs)
        bar = create_tables(
            configuration=configuration,
            data=self.mock_data
        )
        self.assertIsInstance(bar, pd.DataFrame)

        configuration = self.load_configuration(self.configuration_lrg, **kwargs)
        baz = create_tables(
            configuration=configuration,
            data=self.mock_data
        )
        self.assertIsInstance(baz, pd.DataFrame)
