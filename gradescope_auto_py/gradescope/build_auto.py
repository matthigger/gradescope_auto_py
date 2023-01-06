import pathlib
import shutil
import subprocess
import tempfile

from gradescope_auto_py.grader_config import GraderConfig

folder_src = pathlib.Path(__file__).parent


def build_autograder(file_assign, file_zip_out=None, include_folder=False,
                     verbose=True, **kwargs):
    """ builds a directory containing autograder in gradescope format

    Args:
        file_assign (str): assignment file, used to generate a list of asserts
            for points
        file_zip_out (str): name of zip to create (contains setup.sh,
            requirements.txt, run_autograder.py & config.txt).  defaults to
            same name as assignment with zip suffix
        include_folder (bool): if True, all files in folder of file_assign are
            included in autograder zip.  they'll be unpacked next to student
            submitted files (overwritten by student files if name conflicts)
            and available for autograder running
        verbose (bool): toggles message to warn user to set "autograder points"

    Returns:
        file_zip_out (pathlib.Path): zip file created
    """
    # make temp directory (contents will be zipped)
    folder_tmp = pathlib.Path(tempfile.mkdtemp())

    # move file_assign, run_autograder.py & setup.sh to folder
    file_assign = pathlib.Path(file_assign).resolve()
    for file in [folder_src / 'run_autograder',
                 folder_src / 'setup.sh',
                 file_assign]:
        shutil.copy(file, folder_tmp / file.name)

    # build config.json in folder
    grader_config = GraderConfig.from_py(file=file_assign, **kwargs)
    grader_config.to_json(folder_tmp / 'config.json')

    if include_folder:
        # copy all files (except file_run, which should come from student)
        folder_include = folder_tmp / 'include'
        shutil.copytree(file_assign.parent, folder_include)
        shutil.rmtree(folder_include / grader_config.file_run.name)

    # build requirements.txt
    process = subprocess.run(['pipreqs', folder_tmp])
    assert process.returncode == 0, 'problem building requirements.txt'

    # zip it up
    if file_zip_out is None:
        file_zip_out = file_assign.with_suffix('.zip')
    shutil.make_archive(file_zip_out.with_suffix(''), 'zip', folder_tmp)

    # clean up
    shutil.rmtree(folder_tmp)

    if verbose:
        pts_total = sum([afp.pts for afp in grader_config.afp_list])
        print(f'finished building: {file_zip_out}')
        print(f'when uploading zip, be sure to set autograder points to:'
              f' {pts_total}')
        print('(inconsistent values cause "results not formatted correctly")')

    return file_zip_out


if __name__ == '__main__':
    file_assign = '../../test/ex/ex_assign.py'
    build_autograder(file_assign=file_assign, include_folder=True)
