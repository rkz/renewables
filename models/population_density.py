import pandas

from .util import chain, get_data_file_path


def _read_csv(_):
    data = pandas.read_csv(
        get_data_file_path("population-density.csv"),
        skiprows=4,
        usecols=(
            ["Country Code"]
            + [str(year) for year in range(2010, 2020)]
        ),
        index_col=["Country Code"]
    )
    data.index.set_names("code", inplace=True)
    return data


def _mangle_years(input):
    """

    """
    output = pandas.DataFrame()
    output["density"] = input.mean(axis=1)
    return output


population_density = chain(
    None,
    [
        _read_csv,
        _mangle_years,
    ]
)
"""
Index:
  - country `code`

Columns:
  - population `density` in people/km^2
"""
