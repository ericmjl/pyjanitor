import pytest

from janitor.engineering import convert_units


@pytest.mark.engineering
def test_datatypes_check(dataframe):
    # All argument inputs to convert_units() must be strings
    with pytest.raises(TypeError):
        assert dataframe.convert_units(
            123, existing_units="cm", to_units="m", dest_column_name="a_m"
        )
        assert dataframe.convert_units(
            "a", existing_units=123, to_units="m", dest_column_name="a_m"
        )
        assert dataframe.convert_units(
            "a", existing_units="cm", to_units=123, dest_column_name="a_m"
        )
        assert dataframe.convert_units(
            "a", existing_units="cm", to_units="m", dest_column_name=123
        )


@pytest.mark.engineering
def test_numeric_column(dataframe):
    # The animals column contains strings, not numeric values
    with pytest.raises(TypeError):
        assert dataframe.convert_units(
            "animals",
            existing_units="cm",
            to_units="m",
            dest_column_name="len_m",
        )


@pytest.mark.engineering
def test_unit_dimensions(dataframe):
    # Attempts to convert length units to mass
    with pytest.raises(TypeError):
        assert dataframe.convert_units(
            "a", existing_units="cm", to_units="kg", dest_column_name="a_kg"
        )


@pytest.mark.engineering
def test_no_conversion_equal(dataframe):
    df = dataframe.convert_units(
        "a", existing_units="cm", to_units="cm", dest_column_name="a_cm"
    )
    assert all(df["a"] == df["a_cm"])


@pytest.mark.engineering
def test_length_conversion(dataframe):
    df = dataframe.convert_units(
        "a", existing_units="cm", to_units="m", dest_column_name="a_m"
    )
    assert df["a"].sum() == pytest.approx(df["a_m"].sum() * 100.0)


@pytest.mark.engineering
def test_mass_conversion(dataframe):
    df = dataframe.convert_units(
        "a", existing_units="g", to_units="kg", dest_column_name="a_kg"
    )
    assert df["a"].sum() == pytest.approx(df["a_kg"].sum() * 1000.0)


@pytest.mark.engineering
def test_area_conversion(dataframe):
    df = dataframe.convert_units(
        "a", existing_units="cm**2", to_units="m**2", dest_column_name="a_m2"
    )
    assert df["a"].sum() == pytest.approx(df["a_m2"].sum() * (100.0 ** 2))


@pytest.mark.engineering
def test_volume_conversion(dataframe):
    df = dataframe.convert_units(
        "a", existing_units="cm**3", to_units="m**3", dest_column_name="a_m3"
    )
    assert df["a"].sum() == pytest.approx(df["a_m3"].sum() * (100.0 ** 3))
