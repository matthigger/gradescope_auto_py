from math import pi


def get_circle_area(radius):
    return pi * radius ** 2


assert 3 + 2 == 5, 'this assert should be ignored (for points)'
assert get_circle_area(radius=1) == pi, 'get_circle_area(radius=1)  (1 pts)'
assert get_circle_area(radius=10) == 100 * pi, \
    'get_circle_area(radius=1) (2 pts)'
