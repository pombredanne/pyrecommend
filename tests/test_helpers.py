# coding: utf8
"""Tests for helpers module."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import doctest

from pyrecommend import helpers


def test_make_data():
    """make_data() turns a set of lists into a dict matrix."""
    data = helpers.make_data([[3, 5], [20, 50]])
    assert data == {
        1: {1: 3, 2: 5},
        2: {1: 20, 2: 50}
    }


def test_doctests():
    """Ensure doctests work run."""
    failures, _ = doctest.testmod(helpers)
    assert failures == 0
