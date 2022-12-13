from gradescope_auto_py.grader_config import GraderConfig


def test_write_config():
    afp_list = GraderConfig.from_py(file='ex_assign.py')
    afp_s_list = [afp.s for afp in afp_list]

    with open('ex_config.txt', 'r') as f:
        afp_s_list_expected = f.read().split('\n')

    assert afp_s_list == afp_s_list_expected
