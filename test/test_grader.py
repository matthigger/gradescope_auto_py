import gradescope_auto_py as gap
import json

# build config
file_assign = 'ex_assign.py'
grader_config = gap.GraderConfig.from_py(file_assign)

file_submit = 'ex_submit.py'
file_submit_err_syntax = 'ex_submit_err_syntax.py'
file_submit_err_runtime = 'ex_submit_err_runtime.py'
file_prep_expect = 'ex_submit_prep.py'


def test_prep_file():
    s_file_prep, _ = gap.Grader.prep_file(file=file_submit, token='token')
    assert s_file_prep == open(file_prep_expect).read()


def test_grade():
    grader = gap.Grader(grader_config=grader_config)
    grader.grade(file_submit)
    for afp, passes in zip(grader_config, [True, False, False]):
        assert grader.afp_pass_dict[afp] == passes

    # only first assert scores points before runtime error
    grader.grade(file_submit_err_runtime)
    afp_pts_dict_expect = {grader_config[0]: True}
    assert grader.afp_pass_dict == afp_pts_dict_expect


def test_check_for_syntax_error():
    assert gap.Grader.check_for_syntax_error(file=file_submit) is None

    assert gap.Grader.check_for_syntax_error(file=file_submit_err_syntax)


def test_get_json():
    # manually build a "completed" grader
    grader = gap.Grader(grader_config=grader_config)
    for afp in grader_config:
        grader.afp_pass_dict[afp] = True
    grader.stdout = 'test_stdout'
    grader.stderr = 'test_stderr'

    with open('test_get_json.json', 'r') as f:
        json_expected = json.load(f)

    assert json_expected == grader.get_json()
