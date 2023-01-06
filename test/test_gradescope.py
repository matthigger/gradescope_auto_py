import json
import os
import re
import stat
from collections import namedtuple

from gradescope_auto_py.gradescope.build_auto import *

# build autograder zips
file_auto_zip0 = build_autograder(file_template='ex/hw0/template/hw0.py',
                                  include_folder=False)
file_auto_zip1 = build_autograder(file_template='ex/hw1/template/hw1.py',
                                  include_folder=True)

# build test cases
TestCaseFile = namedtuple('TestCaseFile',
                          ['name', 'file_auto_zip', 'submit', 'json_expect'])

test_case_list = [TestCaseFile(name=f'hw0case{idx}',
                               file_auto_zip=file_auto_zip0,
                               submit=f'ex/hw0/submit{idx}',
                               json_expect=f'ex/hw0/expect/case{idx}.json')
                  for idx in range(3)] + \
                 [TestCaseFile(name=f'hw1case{idx}',
                               file_auto_zip=file_auto_zip1,
                               submit=f'ex/hw1/submit{idx}',
                               json_expect=f'ex/hw1/expect/case{idx}.json')
                  for idx in range(3)]


def gradescope_setup(folder_submit, file_auto_zip, folder=None):
    if folder is None:
        # temp directory
        folder = pathlib.Path(tempfile.TemporaryDirectory().name)
    else:
        folder = pathlib.Path(folder)

    # build directories (rm old)
    folder_source = folder / 'source'
    folder_source.mkdir(parents=True)

    # unzip autograder
    shutil.unpack_archive(file_auto_zip,
                          extract_dir=folder_source)

    # move submission into proper spot
    shutil.copytree(folder_submit, folder / 'submission')

    # move run_autograder & setup.sh to proper spot, make executable
    for file in ['run_autograder', 'setup.sh']:
        file = folder / file
        shutil.move(folder_source / file.name, file)

        # chmod +x run_autograder
        st = os.stat(file)
        os.chmod(file, st.st_mode | stat.S_IEXEC)

    return folder


def test_build_autograder():
    for test_idx, test_case in enumerate(test_case_list):
        # setup file structure (as gradescope does)
        folder = gradescope_setup(folder_submit=test_case.submit,
                                  file_auto_zip=test_case.file_auto_zip)

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
        file_json_observe = folder / 'expect' / 'expect.json'
        with open(file_json_observe, 'r') as f:
            json_observed = json.load(f)

        # normalize file names (rm paths from error messages)
        s_output = json_observed['output']
        for file in re.findall('File \"[^ ]+\.py\"', s_output):
            file_new = f'File {pathlib.Path(file).name}'
            s_output = s_output.replace(file, file_new)
        json_observed['output'] = s_output

        if json_observed != json_expected:
            s_json = json.dumps(json_observed, indent=4, sort_keys=True)

        assert json_expected == json_observed, test_case.name

        # cleanup
        shutil.rmtree(str(folder))
