import ast
import secrets
import subprocess
import sys
from copy import copy
from warnings import warn

import pandas as pd

from gradescope_auto_py.assert_for_pts import AssertForPoints, NoPointsInAssert
from gradescope_auto_py.grader_config import GraderConfig


class Grader:
    """ runs a py (or ipynb) file through autograder & formats out (gradescope)

    Attributes:
        afp_pts_dict (dict): keys are AssertForPoints, values are number of
            points earned by student
    """

    def __init__(self, file, grader_config=None, file_prep='prep.py'):
        # prepare submission to run
        s_file_prep, token = self.prep_file(file=file)
        with open(file_prep, 'w') as f:
            print(s_file_prep, file=f, end='')

        # run submission & store stdout & stderr
        result = subprocess.run([sys.executable, file_prep],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        self.stdout = result.stdout.decode('utf-8')
        self.stderr = result.stderr.decode('utf-8')

        # load config from submission (may have been modified!) if needed
        # (safer to pass grader_config built from canonical source assignment)
        if grader_config is None:
            grader_config = GraderConfig.from_py(file)

        # init pts earned to not a number per AssertForPoint
        self.afp_pts_dict = {afp: None for afp in grader_config}

        # record output from stdout and stderr
        self.parse_output(token=token)

    def parse_output(self, token):
        # parse stdout to determine which tests passed
        for line in self.stdout.split('\n'):
            if token not in line:
                # no token in line, ignore it
                continue

            # parse assert for points & passes
            afp_s, s_passes = line.split(token)

            # parse s_passes
            if 'True' in s_passes:
                passes = True
            elif 'False' in s_passes:
                passes = False
            else:
                RuntimeError('invalid assert statement feedback')

            # record
            afp = AssertForPoints(s=afp_s)
            if afp not in self.afp_pts_dict.keys():
                warn(f'assert for points (not in config): {afp.s}')
            else:
                self.afp_pts_dict[afp] = passes

    @classmethod
    def prep_file(cls, file, token=None):
        """ loads file, replaces each assert with grader._assert()

        Args:
            file (path): a student's py file submission
            token (str): some uniquely identifiable (and not easily guessed)
                string.  used to identify which asserts passed when file is run

        Returns:
            s_file_prep (str): string of new python file (prepped)
            token (str): token used
        """
        if token is None:
            token = secrets.token_urlsafe()

        # AssertTransformer converts asserts to grader._assert
        # https://docs.python.org/3/library/ast.html#ast.NodeTransformer
        class AssertTransformer(ast.NodeTransformer):
            def visit_Assert(self, node):
                try:
                    # assert for points, initialize object
                    afp = AssertForPoints(ast_assert=node)
                except NoPointsInAssert:
                    # assert statement, but not for points, leave unchanged
                    return node

                # build new node which prints afp.s, token, whether test passed
                s_grader_assert = f'print(1, 2)'
                new_node = ast.parse(s_grader_assert).body[0]
                new_node.value.args = [ast.Constant(afp.s),
                                       ast.Constant(token),
                                       node.test]

                return new_node

        # parse file, convert all asserts
        with open(file, 'r') as f:
            s_file = f.read()

        assert 'grader_self' not in s_file, "'grader_self' in submission"

        node_root = ast.parse(s_file)
        AssertTransformer().visit(node_root)

        return ast.unparse(node_root), token

    def get_df(self):
        """ gets dataframe.  1 row is an AssertForPoints w/ passes

        Returns:
            df (pd.DataFrame): one col per attribute of AssertForPoints &
                another for 'passes' (see Grader._assert())
        """
        list_dicts = list()
        for afp, passes in self.afp_pts_dict.items():
            d = copy(afp.__dict__)
            d['passees'] = passes
            list_dicts.append(d)

        return pd.DataFrame(list_dicts)

    def get_json(self):
        """ gets json in gradescope format

        https://gradescope-autograders.readthedocs.io/en/latest/specs/#output-format

        """
        # init json
        test_list = list()
        json_dict = {'tests': test_list}

        # add to json (per test case)
        for afp, passes in self.afp_pts_dict.items():
            if passes is None:
                # merge cases: assert not run in submitted -> assert not passed
                passes = False
            test_list.append({'score': afp.pts * passes,
                              'max_score': afp.pts,
                              'name': afp.s})

        return json_dict
