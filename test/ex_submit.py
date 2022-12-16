from math import pi


def get_circle_area(radius):
    # note error: should be pi * radius ** 2
    return pi * radius


# case0: assert not for points
assert 3 + 2 == 5, 'this assert should be ignored (for points)'

# case1: assert for points in config and pass
assert get_circle_area(radius=1) == pi, 'get_circle_area(radius=1)  (1 pts)'

# case 2: assert for points in config and fail
assert get_circle_area(radius=2) == 4 * pi, \
    'get_circle_area(radius=2) (3 pts visible)'

# case 3: assert for points in config but not in student submission
# assert get_circle_area(radius=10) == 100 * pi, \
#     'get_circle_area(radius=10) (2 pts hidden)'

# case 4: assert for points not in config (likely student modification)
assert 3 + 1 == 4, 'this assert was not in config (99999 pts)'
