import warnings
import json
import pandas as pd
import unittest
from src.botech_comparisons import create_tables
warnings.filterwarnings("ignore")


ASSERT_MAP = {
    "self": list,
    "csv": str,
    "html": str,
    "dataframe": pd.DataFrame
}


class TestAPI(unittest.TestCase):
    def load_configuration(
        self,
        filepath: str,
        data_type: str,
        data_format: str
    ) -> dict:
        with open(filepath, "r") as f:
            configuration = json.load(f)
        configuration["data_type"] = data_type
        configuration["data_format"] = data_format
        return configuration

    def setUp(self):
        self.configfuration_with_nothing = "./tests/configuration_with_nothing.json"
        self.configfuration_with_everything = "./tests/configuration_with_everything.json"
        self.configfuration_with_filters = "./tests/configuration_with_filters.json"
        self.configfuration_with_groups = "./tests/configuration_with_groups.json"
        self.mock_data = pd.read_csv("./tests/MOCK_DATA.csv", keep_default_na=False)

    def _assert(self, elements, data_format):
        if isinstance(elements, dict):
            elements = next(iter(elements.values()))
        assert isinstance(elements, ASSERT_MAP[data_format])

    """
    RETURN SELF
    """
    def test_records_self_configuration_with_nothing(self):
        DATA_FORMAT = "self"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_nothing,
            data_type="records",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_records_self_configuration_with_everything(self):
        DATA_FORMAT = "self"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_everything,
            data_type="records",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_records_self_configuration_with_filters(self):
        DATA_FORMAT = "self"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_filters,
            data_type="records",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_records_self_configuration_with_groups(self):
        DATA_FORMAT = "self"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_groups,
            data_type="records",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_comparisons_self_configuration_with_nothing(self):
        DATA_FORMAT = "self"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_nothing,
            data_type="comparisons",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_comparisons_self_configuration_with_everything(self):
        DATA_FORMAT = "self"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_everything,
            data_type="comparisons",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_comparisons_self_configuration_with_filters(self):
        DATA_FORMAT = "self"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_filters,
            data_type="comparisons",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_comparisons_self_configuration_with_groups(self):
        DATA_FORMAT = "self"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_groups,
            data_type="comparisons",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    """
    RETURN CSV
    """
    def test_records_csv_configuration_with_nothing(self):
        DATA_FORMAT = "csv"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_nothing,
            data_type="records",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_records_csv_configuration_with_everything(self):
        DATA_FORMAT = "csv"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_everything,
            data_type="records",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_records_csv_configuration_with_filters(self):
        DATA_FORMAT = "csv"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_filters,
            data_type="records",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_records_csv_configuration_with_groups(self):
        DATA_FORMAT = "csv"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_groups,
            data_type="records",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_comparisons_csv_configuration_with_nothing(self):
        DATA_FORMAT = "csv"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_nothing,
            data_type="comparisons",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_comparisons_csv_configuration_with_everything(self):
        DATA_FORMAT = "csv"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_everything,
            data_type="comparisons",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_comparisons_csv_configuration_with_filters(self):
        DATA_FORMAT = "csv"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_filters,
            data_type="comparisons",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_comparisons_csv_configuration_with_groups(self):
        DATA_FORMAT = "csv"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_groups,
            data_type="comparisons",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    """
    RETURN HTML
    """
    def test_records_html_configuration_with_nothing(self):
        DATA_FORMAT = "html"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_nothing,
            data_type="records",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_records_html_configuration_with_everything(self):
        DATA_FORMAT = "html"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_everything,
            data_type="records",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_records_html_configuration_with_filters(self):
        DATA_FORMAT = "html"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_filters,
            data_type="records",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_records_html_configuration_with_groups(self):
        DATA_FORMAT = "html"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_groups,
            data_type="records",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_comparisons_html_configuration_with_nothing(self):
        DATA_FORMAT = "html"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_nothing,
            data_type="comparisons",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_comparisons_html_configuration_with_everything(self):
        DATA_FORMAT = "html"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_everything,
            data_type="comparisons",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_comparisons_html_configuration_with_filters(self):
        DATA_FORMAT = "html"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_filters,
            data_type="comparisons",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_comparisons_html_configuration_with_groups(self):
        DATA_FORMAT = "html"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_groups,
            data_type="comparisons",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    """
    RETURN DATAFRAME
    """
    def test_records_dataframe_configuration_with_nothing(self):
        DATA_FORMAT = "dataframe"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_nothing,
            data_type="records",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_records_dataframe_configuration_with_everything(self):
        DATA_FORMAT = "dataframe"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_everything,
            data_type="records",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_records_dataframe_configuration_with_filters(self):
        DATA_FORMAT = "dataframe"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_filters,
            data_type="records",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_records_dataframe_configuration_with_groups(self):
        DATA_FORMAT = "dataframe"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_groups,
            data_type="records",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_comparisons_dataframe_configuration_with_nothing(self):
        DATA_FORMAT = "dataframe"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_nothing,
            data_type="comparisons",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_comparisons_dataframe_configuration_with_everything(self):
        DATA_FORMAT = "dataframe"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_everything,
            data_type="comparisons",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_comparisons_dataframe_configuration_with_filters(self):
        DATA_FORMAT = "dataframe"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_filters,
            data_type="comparisons",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)

    def test_comparisons_dataframe_configuration_with_groups(self):
        DATA_FORMAT = "dataframe"
        configuration = self.load_configuration(
            filepath=self.configfuration_with_groups,
            data_type="comparisons",
            data_format=DATA_FORMAT
        )
        elements = create_tables(
            configuration=configuration,
            data=self.mock_data
        )

        self._assert(elements, DATA_FORMAT)
