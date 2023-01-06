from supplement import some_str

print(some_str)


def get_n_lines(file, n=1):
    """ loads a file, returns first line

    Args:
        file (str): file
        n (int): number of lines to read

    Returns:
        n_lines (str): first n lines of the file
    """
    with open(file) as f:
        n_lines = ''.join([f.readline() for _ in range(n)])
    return n_lines


s_expect = '# this is a comment\n\n'
assert get_n_lines(file='supplement.py', n=2) == s_expect, '10 pts'
