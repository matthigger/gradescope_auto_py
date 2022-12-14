import json
import os
import stat

from gradescope_auto_py.gradescope.build_auto import *


def test_build_autograder():
    file_assign = 'ex_assign.py'

    # setup paths
    folder = pathlib.Path('autograder')
    folder_source = folder / 'source'
    file_auto_zip = folder_source / 'auto.zip'

    if folder.exists():
        # delete folder from previous run
        shutil.rmtree(folder)

    # gradescope setup 0: move submission into proper spot
    folder_source.mkdir(parents=True)
    folder_submit = folder / 'submission'
    folder_submit.mkdir()
    shutil.copy(file_assign, folder_submit / file_assign)

    # build autograder zip
    build_autograder(file_assign=file_assign, file_zip_out=file_auto_zip)

    # gradescope setup 1: unzip & move run_autograder
    shutil.unpack_archive(file_auto_zip,
                          extract_dir=file_auto_zip.parent)
    file_run_auto = folder_source.parent / 'run_autograder'
    shutil.move(folder_source / 'run_autograder', file_run_auto)

    # gradescope setup 2: chmod +x
    st = os.stat(file_run_auto)
    os.chmod(file_run_auto, st.st_mode | stat.S_IEXEC)

    # run autograder
    file_run_auto = file_run_auto.resolve()
    subprocess.run(file_run_auto, cwd=file_run_auto.parent)

    # check that results are as expected
    with open('ex_results.json', 'r') as f:
        json_expected = json.load(f)
    with open(folder / 'results' / 'results.json', 'r') as f:
        json_observed = json.load(f)
    assert json_expected == json_observed
