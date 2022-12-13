import gradescope_auto_py as gap

# build config
file_assign = 'ex_assign.py'
grader_config = gap.GraderConfig.from_py(file_assign)

file_submit = 'ex_submit.py'
file_prep_expect = 'ex_submit_prep.py'


def test_prep_file():
    s_file_prep, _ = gap.Grader.prep_file(file=file_submit, token='token')
    assert s_file_prep == open(file_prep_expect).read()


def test_init():
    grader = gap.Grader(file=file_submit, grader_config=grader_config)

    afp_pts_dict_expect = dict(zip(grader_config, [True, False, None]))
    assert grader.afp_pts_dict == afp_pts_dict_expect
