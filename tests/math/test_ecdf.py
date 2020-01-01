import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.pandas import series


@given(s=series(dtype=np.number))
def test_ecdf(s):
    """A simple execution test."""
    x, y = s.ecdf()


@given(s=series(dtype=str))
def test_ecdf_string(s):
    """Test that type enforcement is in place."""
    with pytest.raises(TypeError):
        x, y = s.ecdf()


@given(s=series(elements=st.floats(allow_nan=True)))
def test_ecdf_error_nulls(s):
    """Test that ValueError is raised when nulls are present."""
    if s.isnull().sum() > 0:
        with pytest.raises(ValueError):
            x, y = s.ecdf()
