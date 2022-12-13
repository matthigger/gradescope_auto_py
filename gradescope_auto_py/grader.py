import ast
import pathlib
from copy import copy
from warnings import warn

import numpy as np
import pandas as pd

from gradescope_auto_py.assert_for_pts import AssertForPoints, NoPointsInAssert


class Grader:
    """ runs a py (or ipynb) file through autograder & formats out (gradescope)

    Attributes:
        afp_pts_dict (dict): keys are AssertForPoints, values are number of
            points earned by student
    """

    @classmethod
    def prep_file(cls, file, file_out=None, file_config='grader_config.txt',
                  print_table=True):
        """ modifies a py file to be run by Grader

        1. adds an import and call to Grader.__init__ to build grader
        2. replaces each assert with grader._assert()
        3. adds an export (to json or otherwise) to end of file

        Args:
            file (str): an input .py file (student copy)
            file_out (str): output file.  defaults to appending "_prep" to
                input file.  If False, no output file is written.
            file_config (str): configuration file to be loaded (by loading pt
                values from a config file we ensure students can't modify
                number and type of assert statements in configuration)
            print_table (bool): if True, prepared file prints markdown table of
                results (one row per assert)

        Returns:
            s_file_new (str): string of new python file (prepped)
            file_out (str): path to output file (None if not written)
        """

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

                # replace node with new_node, a call to grader._assert()
                s_grader_assert = f'grader._assert(passes=1, msg=2)'
                new_node = ast.parse(s_grader_assert).body[0]
                new_node.value.keywords[0].value = node.test
                new_node.value.keywords[1].value = ast.Constant(afp.s)

                return new_node

        # parse file, convert all asserts
        with open(file, 'r') as f:
            s_file = f.read()
        node_root = ast.parse(s_file)
        AssertTransformer().visit(node_root)

        # add grader import & init to top of file
        s_start = '\n'.join([
            'import gradescope_auto_py as gap\n',
            f"grader_config = gap.GraderConfig.from_txt('{file_config}')",
            f'grader = gap.Grader(grader_config)\n\n'])

        # add grader export (json) to bottom of file (not impleme'nted yet)
        s_end = ''
        if print_table:
            s_end += '\n'.join([
                '\n#print markdown table of results',
                'df = grader.get_df()',
                "del df['ast_assert']",
                'print(df.to_markdown())'])

        # build string of new file
        s_file_new = '\n'.join([s_start, ast.unparse(node_root), s_end])

        if file_out is False:
            # don't make a new file with string (just return it)
            return s_file_new, None

        if file_out is None:
            # default file_out
            file_out = pathlib.Path(file)
            file_out = file_out.with_stem(file_out.stem + '_prep')

        # write output file
        with open(file_out, 'w') as f:
            print(s_file_new, file=f, end='')

        return s_file_new, file_out

    def __init__(self, grader_config):
        # init pts earned to not a number per AssertForPoint
        self.afp_pts_dict = {afp: np.nan for afp in grader_config}

    def _assert(self, passes, msg):
        """ assign points if assert statement passes

        Args:
            passes (bool): True if assertion passes (False otherwise)
            msg (str): the string attribute of some AssertForPoints object from
                the configuration
        """
        # lookup which assertion is being recorded
        afp = AssertForPoints(s=msg)

        if afp not in self.afp_pts_dict.keys():
            warn(f'assert for points not in rubric: {afp.s}')
            return

        # record if test passes
        self.afp_pts_dict[afp] = passes

    def get_df(self, warn_on_missing=True):
        """ gets dataframe.  1 row is an AssertForPoints w/ passes

        Args:
            warn_on_missing (bool): if True, warns if an AssertForPoints is
                missing

        Returns:
            df (pd.DataFrame): one col per attribute of AssertForPoints &
                another for 'passes' (see Grader._assert())
        """
        list_dicts = list()
        for afp, passes in self.afp_pts_dict.items():
            d = copy(afp.__dict__)
            d['passees'] = passes
            list_dicts.append(d)

            if warn_on_missing and np.isnan(passes):
                warn(f'test missing in submission: {afp.s}')

        return pd.DataFrame(list_dicts)
