import numpy
import pandas

from .util import chain, get_data_file_path


_source = pandas.read_csv(
    get_data_file_path("per-capita-electricity-source-stacked.csv"),
    index_col=["entity", "code", "year"]
)


def _select_last_10_years(source):
    """
    Input: index (entity, code, year), any columns
    Output: same index and columns, select rows where year is between 2010 and 2020
    """

    return source[source.index.isin(range(2010, 2020), level="year")]


def _group_by_code(source):
    """
    Input: index (entity, code, year), any columns
    Output: group by code, average on all columns (ignoring NaN values)
    """

    return source.groupby(level="code").aggregate(numpy.nanmean)


def _build_energy_categories(source):
    """
    Input: any index, columns (coal, gas, oil, nuclear, wind, solar, hydro, other_renewable)
    Output: same index, columns (fossil, nuclear, wind_solar, all_renewable, total)
    """
    
    aggregated = pandas.DataFrame()

    aggregated["fossil"] = source["coal"] + source["gas"] + source["oil"]
    aggregated["nuclear"] = source["nuclear"]
    aggregated["wind_solar"] = source["wind"] + source["solar"]
    aggregated["all_renewable"] = aggregated["wind_solar"] + source["hydro"] + source["other_renewable"]

    aggregated["total"] = aggregated["fossil"] + aggregated["nuclear"] + aggregated["all_renewable"]

    return aggregated


def _kwh_to_mwh(source):
    return source / 1000


electricity_mix = chain(
    _source,
    [
        _select_last_10_years,
        _group_by_code,
        _build_energy_categories,
        _kwh_to_mwh,
    ]
)
"""
Index:
  - country `code`

Columns: electricity consumption in kWh/year/capita, per source
  - `fossil`
  - `nuclear`
  - `wind_solar`
  - `all_renewable` (i.e. hydro + `wind_solar`)
  - `total`
"""
