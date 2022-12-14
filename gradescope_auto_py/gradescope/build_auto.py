import pathlib
import shutil
import subprocess
import tempfile

from gradescope_auto_py.grader_config import GraderConfig

folder_src = pathlib.Path(__file__).parent


def build_autograder(file_assign, file_zip_out=None, include_assign=True,
                     embed_requirements=True):
    """ builds a directory containing autograder in gradescope format

    Args:
        file_assign (str): assignment file, used to generate a list of asserts
            for points
        file_zip_out (str): name of zip to create (contains setup.sh,
            requirements.txt, run_autograder.py & config.txt).  defaults to
            same name as assignment with zip suffix
        include_assign (bool): if True, includes file_assign in the zip.
            (not needed by gradescope, but good book-keeping)
        embed_requirements (bool): if True, avoids using the requirements.txt
            file (gradescope has trouble locating this file)
    """
    list_include = ['run_autograder', 'setup.sh']

    # make temp directory
    folder_tmp = pathlib.Path(tempfile.mkdtemp())

    # build requirements.txt
    file_assign = pathlib.Path(file_assign).resolve()
    if not file_assign.exists():
        raise FileNotFoundError(file_assign)
    file_assign_tmp = folder_tmp / file_assign.name
    shutil.copy(file_assign, file_assign_tmp)
    process = subprocess.run(['pipreqs', folder_tmp])
    assert process.returncode == 0, 'problem building requirements.txt'
    if not include_assign:
        file_assign_tmp.unlink()

    # build config.txt in
    grader_config = GraderConfig.from_py(file=file_assign)
    grader_config.to_txt(folder_tmp / 'config.txt')

    # move run_autograder.py & setup.sh to folder
    for file in list_include:
        shutil.copy(folder_src / file,
                    folder_tmp / file)

    if embed_requirements:
        # load requirements
        f_requirements = folder_tmp / 'requirements.txt'
        with open(f_requirements, 'r') as f:
            s_requirements = f.read()

        # explicitly place in setup.sh
        with open(folder_tmp / 'setup.sh', 'r') as f:
            s_setup_sh = f.read()
        s_requirements = ' '.join(s_requirements.strip().split('\n'))
        s_setup_sh = s_setup_sh.replace('-r requirements.txt', s_requirements)
        with open(folder_tmp / 'setup.sh', 'w') as f:
            print(s_setup_sh, file=f)

        # delete requirements.txt
        f_requirements.unlink()

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
