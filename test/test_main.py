import pathlib
import shutil
import tempfile
from collections import namedtuple

from gradescope_auto_py.__main__ import *


def test_main():
    # copy files into temp folder
    tmp_folder = pathlib.Path(tempfile.TemporaryDirectory().name)
    tmp_folder.mkdir(exist_ok=True)
    shutil.copy('ex/hw0/template/hw0.py', tmp_folder / 'hw0.py')
    shutil.copy('ex/hw0/submit0/hw0.py', tmp_folder / 'hw0.py')

    # prep args
    Args = namedtuple('Args', ['f_template', 'f_submit'])
    args = Args(str(tmp_folder / 'hw0.py'),
                str(tmp_folder / 'hw0.py'))

    # run main
    main(args)

    # ensure output zip and json are created
    assert (tmp_folder / 'hw0.zip').exists()
    assert (tmp_folder / 'hw0_out.json').exists()

    # cleanup
    shutil.rmtree(tmp_folder)
