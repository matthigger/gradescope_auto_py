import json
import pathlib
from collections import Counter

from gradescope_auto_py.assert_for_pts import AssertForPoints


class GraderConfig:
    """ a 'configuration' for an assignment

    Attributes:
        file_run (str): file to run for autograding (often student submitted
            version of assignment)
        afp_list (list): a list of AssertForPoints

    GraderConfig is intended to be created from some canonical copy of the
    HW, rather than a student submission.  this ensures fidelity of all
    asserts (and point values) to the canonical copy.
    """

    def __init__(self, file_run, afp_list):
        self.file_run = pathlib.Path(file_run).name
        self.afp_list = afp_list

    def to_json(self, file):
        """ writes config to txt file (string of each assert on each line)

        Args:
            file (str): file to write configuration to
        """
        json_dict = {'file_run': self.file_run,
                     'afp_list': [afp.s for afp in self.afp_list]}
        with open(file, 'w') as f:
            json.dump(json_dict, f, sort_keys=True, indent=4)

    @classmethod
    def from_json(cls, file):
        """ reads GraderConfig from txt file

        Args:
            file (str): file to write configuration to
        """
        with open(file) as f:
            json_dict = json.load(f)

        afp_list = [AssertForPoints(s=s) for s in json_dict['afp_list']]
        return GraderConfig(file_run=json_dict['file_run'],
                            afp_list=afp_list)

    @classmethod
    def from_py(cls, file, file_run=None):
        """ builds configuration file for assignment from a given rubric

        Args:
            file (str): an input .py file (student or rubric copy)
            file_run (str): name of file to run to perform autograding.  if not
                passed, file name is used

        Returns:
            grader_config (GraderConfig):
        """
        if file_run is None:
            # default file_run name (same as input py file)
            file_run = pathlib.Path(file).name

        # read in only assert for points (strings) from file
        afp_list = list(AssertForPoints.iter_assert_for_pts(file))

        # ensure each is unique
        for afp, count in Counter(afp_list).items():
            assert count < 2, f'non-unique assert found: {afp.s}'

        return GraderConfig(afp_list=afp_list, file_run=file_run)
