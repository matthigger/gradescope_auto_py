import pathlib
import shutil
import subprocess
import tempfile

from gradescope_auto_py.grader_config import GraderConfig

folder_src = pathlib.Path(__file__).parent


def build_autograder(file_assign, file_zip_out=None):
    """ builds a directory containing autograder in gradescope format

    Args:
        file_assign (str): assignment file, used to generate a list of asserts
            for points
        file_zip_out (str): name of zip to create (contains setup.sh,
            requirements.txt, run_autograder.py & config.txt).  defaults to
            same name as assignment with zip suffix
    """
    list_include = ['run_autograder', 'setup.sh']

    # make temp directory
    folder_tmp = pathlib.Path(tempfile.mkdtemp())

    # build requirements.txt
    file_assign = pathlib.Path(file_assign)
    if not file_assign.exists():
        raise FileNotFoundError(file_assign)
    file_assign_tmp = folder_tmp / file_assign.name
    shutil.copy(file_assign, file_assign_tmp)
    process = subprocess.run(['pipreqs', folder_tmp])
    assert process.returncode == 0, 'problem building requirements.txt'
    file_assign_tmp.unlink()

    # build config.txt in
    grader_config = GraderConfig.from_py(file=file_assign)
    grader_config.to_txt(folder_tmp / 'config.txt')

    # move run_autograder.py & setup.sh to folder
    for file in list_include:
        shutil.copy(folder_src / file,
                    folder_tmp / file)

    # zip it up (config, setup.sh & run_autograder)
    if file_zip_out is None:
        file_zip_out = file_assign.with_suffix('')
    file_zip_out = str(file_zip_out)
    if file_zip_out.endswith('.zip'):
        file_zip_out = file_zip_out[:-4]
    shutil.make_archive(file_zip_out, 'zip', folder_tmp)

    # clean up
    shutil.rmtree(folder_tmp)


if __name__ == '__main__':
    file_assign = '../../test/ex_assign.py'
    build_autograder(file_assign=file_assign)
