import ast
import secrets
import subprocess
import sys
import tempfile
from warnings import warn

from gradescope_auto_py.assert_for_pts import AssertForPoints, NoPointsInAssert
from gradescope_auto_py.grader_config import GraderConfig


class Grader:
    """ runs a py (or ipynb) file through autograder & formats out (gradescope)

    Attributes:
        afp_pass_dict (dict): keys are AssertForPoints, values are number of
            points earned by student
        grader_config (GraderConfig): a list of all AssertForPoints which the
            assignment was configured to have (not necessarily all those in the
            student submission)
        stdout (str): stdout from student submission
        stderr (str): stderr from student submission
    """

    def __init__(self, grader_config):
        self.grader_config = grader_config

        self.afp_pass_dict = dict()
        self.stdout = ''
        self.stderr = ''

    def grade(self, file):
        """ grades submission (gets attributes: afp_pass_dict, stdout & stderr)

        Args:
            file (str): student submission for assignment
        """
        # prepare submission file to run
        file_prep = tempfile.NamedTemporaryFile(suffix='.py').name
        s_file_prep, token = self.prep_file(file=file,
                                            afp_list=self.grader_config)
        with open(file_prep, 'w') as f:
            print(s_file_prep, file=f, end='')

        # run submission & store stdout & stderr
        result = subprocess.run([sys.executable, file_prep],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        # record output from stdout and stderr & parse for which asserts pass
        self.stdout = result.stdout.decode('utf-8')
        self.stderr = result.stderr.decode('utf-8')
        self.afp_pass_dict = dict()
        self.parse_output(token=token)

    def parse_output(self, token):
        """ finds which AssertForPoints passes (or not) from stdout

        Args:
            token (str): token which marks output of AssertforPoints in stdout
                (see prep_file())
        """
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
            if afp in self.afp_pass_dict.keys():
                raise RuntimeError(f'duplicated assert-for-points: {afp.s}')
            self.afp_pass_dict[afp] = passes

    @classmethod
    def check_for_syntax_error(cls, file, grader_config=None):
        """ returns json describing syntax error for gradescope (or None)

        Args:
            file (str): submitted file
            grader_config (GraderConfig): list of AssertForPoints in assignment
                (in event of syntax error, we must mark each as a 0 or
                gradescope will give "invalid format" error to json output)

        Returns:
            json_dict (dict): contains key 'output' whose value is a string
                which describes error
        """
        with open(file, 'r') as f:
            s_file = f.read()

        try:
            ast.parse(s_file)
            # no syntax errors found
            return None
        except SyntaxError as err:
            if grader_config is None:
                grader_config = list()
                warn(f'syntax error found in {file}: pass grader_config to '
                     'ensure json_dict is valid input to gradescope')

            s = 'Syntax error found (no points awarded by autograder):'
            s = '\n'.join([s, str(err), err.text])

            msg = 'Error before assert statement run'

            return {'output': s,
                    'tests': [afp.get_json_dict(output=msg)
                              for afp in grader_config]}

    @classmethod
    def prep_file(cls, file, afp_list=None, token=None):
        """ loads file, replaces each assert-for-points with print of results

        every assert-for-points output is a single line which has format

        AssertForPoints.s {token} passes

        where passes is either True or False.  this can be parsed to record
        whether the assert passed (see parse_output())

        Args:
            file (path): a student's py file submission
            afp_list (list): a list of assert for points (if not found, we'll
                add them to the end of the prepped file)
            token (str): some uniquely identifiable (and not easily guessed)
                string.  used to identify which asserts passed when file is run

        Returns:
            s_file_prep (str): string of new python file (prepped)
            token (str): token used
        """
        if token is None:
            token = secrets.token_urlsafe()

        if afp_list is None:
            afp_list = list()

        afp_found = set()

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

                # record which afp were already run (from submission)
                afp_found.add(afp)

                return afp.get_print_ast(token=token)

        # parse file, convert all asserts
        with open(file, 'r') as f:
            s_file = f.read()

        assert 'grader_self' not in s_file, "'grader_self' in submission"

        # replace each assert-for-points with a print statement
        node_root = ast.parse(s_file)
        AssertTransformer().visit(node_root)

        # add in any missing assert-for-points at end of file
        for afp in afp_list:
            if afp in afp_found:
                # assert-for-points already run (in student submission)
                continue

            # assert-for-points not in submission, but in config
            node_root.body.append(afp.get_print_ast(token))

        return ast.unparse(node_root), token

    def get_json(self):
        """ gets json in gradescope format

        https://gradescope-autograders.readthedocs.io/en/latest/specs/#output-format

        """
        s_output = self.stderr

        # init json
        test_list = list()
        json_dict = {'tests': test_list,
                     'output': s_output}

        for afp, passes in self.afp_pass_dict.items():
            if afp in self.grader_config:
                # test case run: configured test case
                kwargs = dict()
            else:
                # test case run: unconfigured test case
                kwargs = {'output': 'assert not found in config (no pts '
                                    'penalized or awarded)',
                          'max_score': 0,
                          'score': 0,
                          'status': 'failed'}
            test_list.append(afp.get_json_dict(passes, **kwargs))

        # add configured test cases never run
        for afp in self.grader_config:
            if afp not in self.afp_pass_dict.keys():
                msg = 'Error before assert statement run'
                test_list.append(afp.get_json_dict(output=msg,
                                                   status='failed',
                                                   passes=0))

        return json_dict
