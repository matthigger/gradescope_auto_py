import pathlib
import shutil
import subprocess
import tempfile

from gradescope_auto_py.grader_config import GraderConfig

folder_src = pathlib.Path(__file__).parent


def build_autograder(file_assign, file_zip_out=None, file_include_list=None,
                     verbose=True):
    """ builds a directory containing autograder in gradescope format

    Args:
        file_assign (str): assignment file, used to generate a list of asserts
            for points
        file_zip_out (str): name of zip to create (contains setup.sh,
            requirements.txt, run_autograder.py & config.txt).  defaults to
            same name as assignment with zip suffix
        file_include_list (list): a list of files to include in zip.  these
            will be copied over adjacent to the student submitted version of
            file_assign (allows importing from another local file)
        verbose (bool): toggles message to warn user to set "autograder points"

    Returns:
        file_zip_out (pathlib.Path): zip file created
    """
    if file_include_list is None:
        file_include_list = list()

    list_include = [folder_src / 'run_autograder',
                    folder_src / 'setup.sh',
                    file_assign] + file_include_list

    # make temp directory
    folder_tmp = pathlib.Path(tempfile.mkdtemp())

    # move run_autograder.py & setup.sh to folder
    for file in list_include:
        file = pathlib.Path(file)
        shutil.copy(file, folder_tmp / file.name)

    # build requirements.txt
    process = subprocess.run(['pipreqs', folder_tmp])
    assert process.returncode == 0, 'problem building requirements.txt'

    # build config.txt in folder
    grader_config = GraderConfig.from_py(file=file_assign)
    grader_config.to_txt(folder_tmp / 'config.txt')

    # build other_files.txt in folder
    if file_include_list:
        file_link_list = [pathlib.Path(f).name for f in file_include_list]
        with open(folder_tmp / 'also_include.txt', 'w') as f:
            print('\n'.join(file_link_list), file=f)

    # zip it up (config, setup.sh & run_autograder)
    if file_zip_out is None:
        file_zip_out = file_assign
    file_zip_out = pathlib.Path(file_zip_out).with_suffix('')
    shutil.make_archive(file_zip_out, 'zip', folder_tmp)
    file_zip_out = pathlib.Path(file_zip_out).with_suffix('.zip')

    # clean up
    shutil.rmtree(folder_tmp)

    if verbose:
        pts_total = sum([afp.pts for afp in grader_config])
        print(f'finished building: {file_zip_out}')
        print(f'when uploading zip, be sure to set autograder points to:'
              f' {pts_total}')
        print('(inconsistent values cause "results not formatted correctly")')

    return file_zip_out


if __name__ == '__main__':
    file_assign = '../../test/ex_assign.py'
    build_autograder(file_assign=file_assign)
