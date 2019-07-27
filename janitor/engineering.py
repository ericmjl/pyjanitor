"""
Engineering-specific data cleaning functions.
"""

import numpy as np
import pandas as pd
import pandas_flavor as pf

from janitor import check

from .utils import import_message

try:
    import unyt
except ImportError:
    import_message("engineering", "unyt", "conda install -c conda-forge unyt")


@pf.register_dataframe_method
def convert_units(
    df: pd.DataFrame,
    column_name: str = None,
    existing_units: str = None,
    to_units: str = None,
    dest_column_name: str = None,
) -> pd.DataFrame:
    """
    Uses the unyt package to convert a column of numeric values
    from one unit to another.

    Unit conversion can only take place if the existing_units and
    to_units are of the same type (e.g., temperature or pressure).
    The provided unit types can be any unit name or alternate name provided
    in the unyt package's Listing of Units table:
    https://unyt.readthedocs.io/en/stable/unit_listing.html#unit-listing.

    Volume units are not provided natively in unyt.  However, exponents are
    supported, and therefore some volume units can be converted.  For example,
    a volume in cubic centimeters can be converted to cubic meters using
    existing_units='cm**3' and to_units='m**3'.

    This method mutates the original DataFrame.

    Functional usage example:

    .. code-block:: python

        import pandas as pd
        import janitor.engineering

        df = pd.DataFrame(...)

        df = janitor.engineering.convert_units(
            df=df,
            column_name='temp_F',
            existing_units='degF',
            to_units='degC',
            dest_column_name='temp_C'
        )

    Method chaining usage example:

    .. code-block:: python

        import pandas as pd
        import janitor.engineering

        df = pd.DataFrame(...)

        df = df.convert_units(
            column_name='temp_F',
            existing_units='degF',
            to_units='degC',
            dest_column_name='temp_C'
        )

    :param df: A pandas dataframe.
    :param column_name: Name of the column containing numeric
        values that are to be converted from one set of units to another.
    :param existing_units: The unit type to convert from.
    :param to_units: The unit type to convert to.
    :param dest_column_name: The name of the new column containing the
        converted values that will be created.
    """

    # Check all inputs are correct data type
    check("column_name", column_name, [str])
    check("existing_units", existing_units, [str])
    check("to_units", to_units, [str])
    check("dest_column_name", dest_column_name, [str])

    # Check that column_name is a numeric column
    if not np.issubdtype(df[column_name].dtype, np.number):
        raise TypeError(f"{column_name} must be a numeric column.")

    # Check that existing_units and to_units are of the same type
    existing_type = eval("unyt." + existing_units + ".dimensions")
    to_type = eval("unyt." + to_units + ".dimensions")
    if existing_type != to_type:
        raise TypeError(
            f"{existing_units} are not of the same type as {to_units}."
            f"{existing_units} are of type {existing_type}."
            f"{to_units} are of type {to_type}."
        )

    original_vals = df[column_name].values * eval("unyt." + existing_units)
    converted_vals = original_vals.to(to_units)
    df[dest_column_name] = np.array(converted_vals)

    return df
