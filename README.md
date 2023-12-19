# botech comparisons
[![asciicast](https://asciinema.org/a/tbWegFJBh7Rk7bBg6VRZ2LAgF.svg)](https://asciinema.org/a/tbWegFJBh7Rk7bBg6VRZ2LAgF)
## Description
Generate tables of results, which are extracted from a data source.
- These can be different datatypes: 
    - comparison: (the most common) two scenarios, compared by effects, costs and cost-effectiveness
    - record: the individual records, with effects and costs
- These can be presented by: region, income, appendix 3 status, author, intervention, *or any combination of these*
- These can be filtered by: region, income, appendix 3 status, author, intervention, scenario, *or any combination of these*
- These can be in various formats: csv, html, pandas dataframes, python lists.

Part of the Botech ecosystem, written by [Forecast Health Australia](https://forecasthealth.org)

## Context
This repository was created because we were generating a lot of health-economic model data, often from different sources, and we wanted to compare it in lots of ways.  
I was frustrated with hard coding comparisons, and felt there was a better way to do it. There are lots of solutions to this type of thing, but it seemed marginally easier to write a new package that we could modify as our use cases changed. 

## How I use it
1. Have some general mechanism to convert modelling results to a `csv` of [Records](#data-types)
2. Generate a [configuration file](#basic-example)
3. Invoke this package, either by installing it, or running [the main script](./scripts/main.py) and passing your files as arguments.
4. Use the results however you'd like e.g.
    - Render the results as an html and host them on a website

## Installation
### Requirements
- Python (built with 3.10.12)
- [botech-metadata](https://github.com/ForecastHealth/botech-metadata)
- pandas

### Setup
- `git clone https://github.com/ForecastHealth/botech-comparisons.git`
- `pip install -r requirements.txt` (use a virtual environment)


## Usage
### Data Types
There are two python `dataclasses` and one `enum` which are important to understand: The `Record`, the `Comparison` and the `Filter`.
You can find their definitions in the [datatypes module](./src/botech_comparisons/datatypes.py).

In particular:
- The `Record` is important, because we expect the underlying database *to be a `CSV` file with the schema of a `Record`*
- The `Filter` is important, because you can filter and group using these elements.

### The configuration file
Write a `config.json`, which defines the following:
- `data_type`: the type of table you want to return (explained below)
    - `blueprint` (note - this is probably not useful unless you already know what it is)
    - `filtered_records` (individual records)
    - `comparisons` (comparisons of records - probably what you want)
- `data_format`: the format of the table you want to return `csv`, `html`, `dataframe`, or `self`.
    - `dataframe` is a `pandas.DataFrame`
    - `self` is a `list` of the [data type](#data-types)
- `scenarios` is a list of *exactly two* elements, where each element corresponds to a `scenario`. These must be labelled in your dataset, e.g. `baseline` and `scale-up`
- `groups` is a list of lists, with each nested list being the ways you want to present the data. For instance, if you have list `["region", "income"]`, this means you want the data to be presented *by region by income* e.g. "North America x High Income", "Oceania x Low Income", etc.
- `filters` are dictionary of [Filters](#data-types) where the value is a list of values that you want to include. e.g.
    - `"income": ["HIGH INCOME"]` will only include results from high income countries
    - `"country": ["BRA", "MOZ"]` will only include results from Brazil and Mozambique
    - etc
    
```
{
	"data_type": "comparisons",
	"data_format": "html",
	"scenarios": ["baseline", "scaleup"],
	"groups": [
		["region", "income"]
	],
	"filters": {
		"income": ["HIGH INCOME"],
		"intervention": [0]
	}
}
```
### The API
Please refer to [the __init__.py](./src/botech_comparisons/__init__.py) to read the high-level api `create_tables()`. 
The configuration can be created by parsing a JSON configuration using `parse_configurations` and the `data` will need to be provided by the user and parsed using something like `pandas.read_csv()`.


## Contributing
Feel free to fork, or submit a user issue.
If you'd like to be added as a contributor, please message me, or email our website [Forecast Health Australia](https://forecasthealth.org)


## Tests
Tests are built with `unittest` and can be run locally using
```
python -m unittest discover tests
```
from the root directory.

## Authors
Rory Watts, [Forecast Health Australia](https://forecasthealth.org)

## License
This repository is licensed under the [Apache 2.0 License](./LICENSE).

## Contact Information
Please 

