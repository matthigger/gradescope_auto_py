import json
import os
import re
import stat
from collections import namedtuple

from gradescope_auto_py.gradescope.build_auto import *

# build test cases
TestCaseFile = namedtuple('TestCaseFile', ['submit', 'json_expect'])
test_case_list = [TestCaseFile(submit=f'ex/hw0/submit{idx}/hw0.py',
                               json_expect=f'ex/hw0/expect/case{idx}.json')
                  for idx in range(3)]


def gradescope_setup(f_submit, file_auto_zip, folder=None, rename_submit=True):
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

    # unzip autograder
    shutil.unpack_archive(file_auto_zip,
                          extract_dir=folder_source)

    # move submission into proper spot
    if rename_submit:
        # rename submission to follow proper name (expected from config)
        grader_config = GraderConfig.from_json(folder_source / 'config.json')
        name = grader_config.file_run
    else:
        # use given name
        name = pathlib.Path(f_submit).name
    shutil.copy(f_submit, folder_submit / name)

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
    file_auto_zip = build_autograder(file_template='ex/hw0/template/hw0.py')

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
        result = subprocess.run(file, cwd=file.parent,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        stderr = result.stderr.decode('utf-8')
        assert stderr == '', f'error in run_autograder: {stderr}'

        # check that expect are as expected
        with open(test_case.json_expect, 'r') as f:
            json_expected = json.load(f)
        with open(folder / 'expect' / 'expect.json', 'r') as f:
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
