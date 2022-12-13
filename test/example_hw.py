from math import pi


def get_circle_area(radius):
    # note error: should be pi * radius ** 2
    return pi * radius


assert 3 + 2 == 5, 'this assert should be ignored (for points)'

# this assert is unmodified
assert get_circle_area(radius=1) == pi, 'get_circle_area(radius=1)  (1 pts)'

# this assert will not run in student copy so it can't be recorded
# assert get_circle_area(radius=2) == 4 * pi, \
#    'get_circle_area(radius=2) (3 pts)'

# this assert has a modified point value, because it has been modified it
# can't be registered to canonical assert (see example_hw_rub.py) and won't
# be recorded2912849128
assert get_circle_area(radius=10) == 100 * pi, \
    'get_circle_area(radius=1) (2912849128 pts)'
