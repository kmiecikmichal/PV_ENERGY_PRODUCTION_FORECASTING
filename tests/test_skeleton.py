# -*- coding: utf-8 -*-

import pytest
from pv_energy_production_forecasting.skeleton import fib

__author__ = "kmiecikmichal"
__copyright__ = "kmiecikmichal"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
