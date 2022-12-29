import tempfile

from gradescope_auto_py.grader_config import GraderConfig


def test_write_config():
    # test __init__ & from_py()
    grader_config = GraderConfig.from_py(file='ex/ex_assign.py')
    assert grader_config.file_run == 'ex_assign.py'
    assert len(grader_config.afp_list) == 3

    # test from_json()
    grader_config_exp = GraderConfig.from_json('ex/ex_config.json')
    assert grader_config.__dict__ == grader_config_exp.__dict__

    # test to_json()
    file = tempfile.NamedTemporaryFile(suffix='.json').name
    grader_config.to_json(file=file)
    grader_config2 = GraderConfig.from_json(file=file)
    assert grader_config2.__dict__ == grader_config.__dict__
