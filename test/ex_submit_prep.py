from math import pi

def get_circle_area(radius):
    return pi * radius
assert 3 + 2 == 5, 'this assert should be ignored (for points)'
print("assert get_circle_area(radius=1) == pi, 'get_circle_area(radius=1)  (1 pts)'", 'token', get_circle_area(radius=1) == pi)
print("assert get_circle_area(radius=2) == 4 * pi, 'get_circle_area(radius=2) (3 pts visible)'", 'token', get_circle_area(radius=2) == 4 * pi)
print("assert 3 + 1 == 4, 'this assert was not in config (99999 pts)'", 'token', 3 + 1 == 4)