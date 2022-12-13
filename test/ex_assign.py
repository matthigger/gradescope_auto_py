# rubric copy (canonical copy which has all asserts & points)
from math import pi


def get_circle_area(radius):
    pass


assert 3 + 2 == 5, 'this assert should be ignored (not for points)'
assert get_circle_area(radius=1) == pi, 'get_circle_area(radius=1)  (1 pts)'
assert get_circle_area(radius=2) == 4 * pi, \
    'get_circle_area(radius=2) (3 pts)'
assert get_circle_area(radius=10) == 100 * pi, \
    'get_circle_area(radius=10) (2 pts)'
