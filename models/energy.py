import pandas
import numpy

from .util import chain, get_data_file_path


def _pick_columns_and_index(input):
    output = pandas.DataFrame()

    output["code"] = input["Code"]
    output["year"] = input["Year"]
    output["energy"] = input["Primary energy consumption per capita (kWh/person)"]
    
    return output.set_index(["code", "year"])


def _average_of_last_10_years(input):
    last_10_years = input[input.index.isin(range(2010, 2020), level="year")]
    return last_10_years.groupby(level="code").aggregate(numpy.nanmean)


def _kwh_to_mwh(input):
    return input / 1000


_source = pandas.read_csv(get_data_file_path("energy.csv"))

energy = chain(
    _source,
    [
        _pick_columns_and_index,
        _average_of_last_10_years,
        _kwh_to_mwh,
    ]
)
"""
Index:
  - country `code`

Columns:
  - primary `energy` consumption in kWh/person/year over last 10 years
"""
