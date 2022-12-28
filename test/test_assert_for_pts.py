import json

from gradescope_auto_py.assert_for_pts import *

s = "assert 3+2==5, 'addition fail (3 pts)'"


def test_init():
    kwargs_list = [dict(s=s), dict(ast_assert=ast.parse(s).body[0])]

    for kwargs in kwargs_list:
        afp = AssertForPoints(**kwargs)
        assert afp.s == "assert 3 + 2 == 5, 'addition fail (3 pts)'"
        assert afp.pts == 3


def test_eq():
    afp = AssertForPoints(s=s)
    assert afp == afp


def test_iter_assert_for_pts():
    with open('ex_config.json', 'r') as f:
        afp_set_expect = set(json.load(f)['afp_list'])

    afp_iter = AssertForPoints.iter_assert_for_pts('ex_assign.py')
    afp_set = set([afp.s for afp in afp_iter])

    assert afp_set == afp_set_expect
