import pathlib
import shutil
import tempfile
from collections import namedtuple

from gradescope_auto_py.__main__ import *


def test_main():
    # move example to new folder
    tmp_folder = pathlib.Path(tempfile.TemporaryDirectory().name)
    folder_ex = pathlib.Path('ex/hw1/template')
    shutil.copytree(folder_ex, tmp_folder)

    # prep args
    Args = namedtuple('Args', ['f_template', 'f_submit',
                               'file_run', 'include_folder'])
    args = Args(f_template=str(tmp_folder / 'hw1.py'),
                f_submit=str(tmp_folder / 'hw1.py'),
                file_run='asdf.py',
                include_folder=True)

    # run main
    main(args)

    # ensure output zip and json are created
    assert (tmp_folder / 'hw1.zip').exists()
    assert (tmp_folder / 'hw1_out.json').exists()

    # cleanup
    shutil.rmtree(tmp_folder)
