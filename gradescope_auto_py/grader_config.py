from collections import Counter

from gradescope_auto_py.assert_for_pts import AssertForPoints


class GraderConfig(list):
    """ a 'configuration' for an assignment, a list of AssertForPoints

    GraderConfig is intended to be created from some canonical copy of the
    HW, rather than a student submission.  this ensures fidelity of all
    asserts (and point values) to the canonical copy.
    """

    def to_txt(self, file):
        """ writes config to txt file (string of each assert on each line)

        Args:
            file (str): file to write configuration to
        """
        with open(str(file), 'w') as f:
            print('\n'.join([afp.s for afp in self]), file=f)

    @classmethod
    def from_txt(cls, file):
        """ reads GraderConfig from txt file

        Args:
            file (str): file to write configuration to
        """
        with open(file, 'r') as f:
            afp_s_list = f.read().strip().split('\n')

        return GraderConfig([AssertForPoints(s=s) for s in afp_s_list])

    @classmethod
    def from_py(cls, file):
        """ builds configuration file for assignment from a given rubric

        Args:
            file (str): an input .py file (student or rubric copy)

        Returns:
            grader_config (GraderConfig):
        """
        # read in only assert for points (strings) from file
        grader_config = GraderConfig(AssertForPoints.iter_assert_for_pts(file))

        # ensure each is unique
        for afp, count in Counter(grader_config).items():
            assert count < 2, f'non-unique assert found: {afp.s}'

        return grader_config
