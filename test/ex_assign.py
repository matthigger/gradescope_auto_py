# rubric copy (canonical copy which has all asserts & points)
from math import pi

import numpy as np
import pandas as pd

# silly statements to justify including numpy and pandas
# (their inclusion tests detection & inclusion of modules from this file in
# the python interpreter on gradescope)
np.nan
pd.DataFrame


def get_circle_area(radius):
    pass


assert 3 + 2 == 5, 'this assert should be ignored (not for points)'
assert get_circle_area(radius=1) == pi, 'get_circle_area(radius=1)  (1 pts)'
assert get_circle_area(radius=2) == 4 * pi, \
    'get_circle_area(radius=2) (3 pts visible)'
assert get_circle_area(radius=10) == 100 * pi, \
    'get_circle_area(radius=10) (2 pts hidden)'
