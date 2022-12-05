from collections.abc import Iterable

import matplotlib
import pandas


matplotlib.colormaps.register(
    matplotlib.colormaps["RdYlGn"].reversed(),
    name="ghg"
)


def scatter_plot(
    data_frame: pandas.DataFrame,
    clabel: str = None,
    annotations: Iterable[str] = None,
    annotations_delta_x: int = 1,
    annotations_delta_y: int = 1,
    **kwargs
):
    """
    Run `data_frame.plot.scatter` with `**kwargs` and additional features:

    - `clabel`: label of the colorbar
    - `annotations`: texts to write aside data points
    """

    plot = data_frame.plot.scatter(**kwargs)

    if clabel is not None:
        plot.get_figure().get_axes()[1].set_ylabel(clabel)
    
    if annotations is not None:
        for index, text in enumerate(annotations):
            _x = data_frame.iloc[index][kwargs["x"]] + annotations_delta_x
            _y = data_frame.iloc[index][kwargs["y"]] + annotations_delta_y
            plot.annotate(text, (_x, _y))
