"""An environment script to make shell usage easy.

Use::

    python --interactive recommend_shell.py

"""
# pylint: disable=unused-wildcard-import,wildcard-import,invalid-name
import os.path

import movielens
from recommendations import *

from critics import critics
movies = invert_data(critics)
movielens = movielens.load_movielens_data('ml-100k')
