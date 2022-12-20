import json
import os
import re
import stat
from collections import namedtuple

from gradescope_auto_py.gradescope.build_auto import *

TestCaseFile = namedtuple('TestCaseFile', ['submit', 'json_expect'])

test_case_list = [TestCaseFile(submit='ex_submit.py',
                               json_expect='ex_results.json'),
                  TestCaseFile(submit='ex_submit_err_runtime.py',
                               json_expect='ex_results_err_runtime.json'),
                  TestCaseFile(submit='ex_submit_err_syntax.py',
                               json_expect='ex_results_err_syntax.json')]


def gradescope_setup(f_submit, file_auto_zip, folder=None):
    if folder is None:
        # temp directory
        folder = pathlib.Path(tempfile.TemporaryDirectory().name)
    else:
        folder = pathlib.Path(folder)

    # build directories (rm old)
    folder_source = folder / 'source'
    folder_submit = folder / 'submission'
    folder_source.mkdir(parents=True)
    folder_submit.mkdir()

    # move submission into proper spot
    shutil.copy(f_submit, folder_submit / pathlib.Path(f_submit).name)

    # unzip autograder
    shutil.unpack_archive(file_auto_zip,
                          extract_dir=folder_source)

    # move run_autograder & setup.sh to proper spot, make executable
    for file in ['run_autograder', 'setup.sh']:
        file = folder / file
        shutil.move(folder_source / file.name, file)

        # chmod +x run_autograder
        st = os.stat(file)
        os.chmod(file, st.st_mode | stat.S_IEXEC)

    return folder


def test_build_autograder():
    # build autograder zip
    file_auto_zip = build_autograder(file_assign='ex_assign.py',
                                     file_include_list=['ex_other_file.py'])

    for test_idx, test_case in enumerate(test_case_list):
        # setup file structure (as gradescope does)
        folder = gradescope_setup(f_submit=test_case.submit,
                                  file_auto_zip=file_auto_zip)

        if test_idx == 0:
            # run setup.sh
            file = (folder / 'setup.sh').resolve()
            subprocess.run(file, cwd=file.parent)

        # run run_autograder
        file = (folder / 'run_autograder').resolve()
        subprocess.run(file, cwd=file.parent)

        # check that results are as expected
        with open(test_case.json_expect, 'r') as f:
            json_expected = json.load(f)
        with open(folder / 'results' / 'results.json', 'r') as f:
            json_observed = json.load(f)

        # normalize file names (rm tempfile from error message)
        s_output = json_observed['output']
        s_list = re.findall('File \".+\.py\"', json_observed['output'])
        if s_list:
            assert len(s_list) == 1, 'non-unique file name in regex'
            json_observed['output'] = s_output.replace(s_list[0],
                                                       'File "submit_prep.py"')

        assert json_expected == json_observed, f'test case {test_idx}'

        # cleanup
        shutil.rmtree(str(folder))
