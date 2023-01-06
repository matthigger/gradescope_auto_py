# Gradescope Autograder for Python

## Installation

    $ pip install gradescope_auto_py

## Usage

1. Define assert-for-points by adding a point value to any `assert` statements in a template copy of the assignment (e.g. [example_hw.py](test/ex/example_hw.py))

```python
assert get_area(radius=1) == pi, 'case0: area from r=1 (2 pts)'
```

2. Build an autograder in [gradescope's autograder format](https://gradescope-autograders.readthedocs.io/en/latest/specs/) by processing this template file:

```
$ python3 -m gradescope_auto_py example_hw.py
```

3. Upload this `.zip` file to a gradescope "programming assignment".  Student submissions will be automatically graded upon submission.

## Notes

- When initializing the assignment in gradescope, be sure to provide a value
  for "autograder points" which is the sum of points in every
  assert-for-points (otherwise submissions will yield a "not formatted
  correctly" response).

- You can control when (and if) a student sees output of every
  assert-for-points by
  adding [a visibility setting ('visible', 'hidden', 'after_due_date', 'after_published')](https://gradescope-autograders.readthedocs.io/en/latest/specs/#controlling-test-case-visibility)
  after the points value within an assert statement:

```python
assert get_area(radius=1) == pi, 'case0: area from r=1 (2 pts hidden)'
```

If no visibility is specified, the assert defaults to 'visible'. Don't forget,
to truly "hide" an assert from a student you'll have to remove it from the
blank copy of the assignment given to students too :)

- We automatically identify the modules to be installed on gradescope's
  interpreter via the blank instructor copy of assignment. Student submissions which import a module outside of these cannot be autograded (
  see [#4](https://github.com/matthigger/gradescope_auto_py/issues/4))

- By using the `--supplement` flag, you can include "supplementary files" which are copied alongside student submission before autograding.  Doing so allows you to ensure all submissions have access to the same "extra" files (expected test case output, another python package etc).  Every file in the same folder as the template file is considered supplementary (except `.zip` files)  

## Configured asserts vs submitted asserts

The set of all assert-for-points is defined by the template version of the assignment passed to `build_autograder()`.  A submitted assignment, however, may not have the same set of assert-for-points in the body of the code:

- If a submission is missing an assert-for-points from the configuration, it is appended to the end of the submitted file.
    - This is helpful if you wish to hide an assert-for-points from students.
- If a submission matches an assert-for-points from the configuration, it is run within the body of the student's submission.
    - This is helpful to control the location of the assert within the student's submission.
- If a non-matching assert-for-points appears in student copy, no points are
  awarded.

## See also

- [Otter-grader](https://otter-grader.readthedocs.io/en/latest/)
- [Gradescope-utils](https://github.com/gradescope/gradescope-utils)
