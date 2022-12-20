import ast
import re

from gradescope_auto_py.visibility import Visibility


class NoPointsInAssert(Exception):
    pass


class AssertForPoints:
    """ an assertion to be evaluated for points

    Attributes:
        pts (float): number of points assert is worth
        ast_assert (ast.Assert): Assert statement
        s (str): string of assert statement
        viz (Visibility): visibility setting (see Visibility)

    >>> afp = AssertForPoints(s="assert 3+2==5, 'addition fail (3 pts)'")
    >>> afp.s
    "assert 3 + 2 == 5, 'addition fail (3 pts)'"
    >>> afp.pts
    3.0
    >>> AssertForPoints(s="assert 3+2==5, 'addition fail'")
    Traceback (most recent call last):
     ...
    assert_for_pts.NoPointsInAssert: assert 3 + 2 == 5, 'addition fail'
    """

    @classmethod
    def iter_assert_for_pts(cls, file):
        """ iterates through all assert_for_pts instances in a file

        Yields:
            assert_for_pts (AssertForPoints):
        """
        with open(str(file), 'r') as f:
            s_file = f.read()

        ast_root = ast.parse(s_file)
        for ast_statement in ast.walk(ast_root):
            if not isinstance(ast_statement, ast.Assert):
                continue

            try:
                yield AssertForPoints(ast_assert=ast_statement)
            except NoPointsInAssert:
                continue

    def __init__(self, s=None, ast_assert=None):
        assert (s is None) != (ast_assert is None), \
            'either s xor ast_assert required'

        # ast_assert
        if s is not None:
            self.ast_assert = ast.parse(s).body[0]
        else:
            self.ast_assert = ast_assert
        assert isinstance(self.ast_assert, ast.Assert)

        # normalize string (spaces between operators etc removed via unparse)
        self.s = ast.unparse(self.ast_assert)

        # get points
        if self.ast_assert.msg is None:
            # no string in assert
            raise NoPointsInAssert(self.s)
        s = ast.unparse(self.ast_assert.msg)
        match_list = re.findall(r'\d+\.?\d* pts', s)
        if not len(match_list) == 1:
            raise NoPointsInAssert(self.s)
        s_pts = match_list[0]
        self.pts = float(s_pts.split(' ')[0])

        # parse visibility setting
        s_viz = self.ast_assert.msg.s.split(s_pts)[1]
        self.viz = Visibility.parse(s_viz)
        if self.viz is None:
            # default to visible
            self.viz = Visibility.VISIBLE

    def get_json_dict(self, passes=False, **kwargs):
        """ builds dict of a single `test` (see key "tests" in link)

        https://gradescope-autograders.readthedocs.io/en/latest/specs/#output-format

        Args:
            passes (bool): scales points (all pts if True, no points if False)
            kwargs: added (overwritten) values
        """
        json_dict = {'score': self.pts * passes,
                     'max_score': self.pts,
                     'name': self.s,
                     'visibility': self.viz.value}
        json_dict.update(kwargs)
        return json_dict

    def get_print_ast(self, token):
        # build new node which prints afp.s, token, whether test passed
        s_grader_assert = f'print(1, 2)'
        new_node = ast.parse(s_grader_assert).body[0]
        new_node.value.args = [ast.Constant(self.s),
                               ast.Constant(token),
                               self.ast_assert.test]
        return new_node

    def __hash__(self):
        return hash(self.s)

    def __eq__(self, other):
        return isinstance(other, AssertForPoints) and self.s == other.s
