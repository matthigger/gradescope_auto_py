import pathlib
import shutil
from collections import namedtuple

from gradescope_auto_py.__main__ import *


def test_main():
    # copy files into temp folder
    tmp_folder = pathlib.Path('.').resolve() / 'tmp'
    tmp_folder.mkdir(exist_ok=True)
    shutil.copy('ex_assign.py', tmp_folder / 'ex_assign.py')
    shutil.copy('ex_submit.py', tmp_folder / 'ex_submit.py')

    # prep args
    Args = namedtuple('Args', ['f_assign', 'f_submit'])
    args = Args(str(tmp_folder / 'ex_assign.py'),
                str(tmp_folder / 'ex_submit.py'))

    # run main
    main(args)

    # ensure output zip and json are created
    assert (tmp_folder / 'ex_assign.zip').exists()
    assert (tmp_folder / 'ex_submit_out.json').exists()

    # cleanup
    shutil.rmtree(tmp_folder)
