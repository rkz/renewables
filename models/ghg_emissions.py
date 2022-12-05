import numpy
import pandas

from .util import get_data_file_path


def _read_csv():
    """
    Output: index (`code`, `year`), columns (`ghg_emissions`)
    """
    data = pandas.read_csv(
        get_data_file_path("ghg-emissions.csv"),
        usecols=["Code", "Year", "Annual consumption-based CO₂ emissions (per capita)"],
        index_col=["Code", "Year"]
    )
    data.index.set_names(["code", "year"], inplace=True)
    data.columns = ["ghg_emissions"]
    return data


def _average_over_last_10_years(input):
    """
    Output: index `code`, columns `ghg_emissions`
    """
    return input.groupby(level="code").aggregate(numpy.nanmean)


data = _read_csv()
data = _average_over_last_10_years(data)

ghg_emissions = data
"""
Index:
  - country `code`

Columns:
  - `ghg_emissions` in tCO2e/year/person averaged over last 10 years
"""
