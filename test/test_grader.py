import gradescope_auto_py as gap


def test_grader():
    file = 'example_hw.py'
    file_config = 'example_hw_config.txt'

    # prep file
    s_file_prep, _ = gap.Grader.prep_file(file=file,
                                          file_config=file_config,
                                          file_out=False,
                                          print_table=True)

    # expected file
    with open('example_hw_prep.py', 'r') as f:
        s_file_prep_expected = f.read()

    assert s_file_prep == s_file_prep_expected
