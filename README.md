# Gradescope Autograder for Python

## Installation

    $ pip install gradescope_auto_py

## Usage

1. Define assert-for-points by adding a point value to any `assert` statements in a blank copy of the assignment (
   e.g. [ex_assign.py](test/ex_assign_pretty.py))

```python
assert get_area(radius=1) == pi, 'case0: area from r=1 (2 pts)'
```

2. Build an autograder in [gradescope's autograder format](https://gradescope-autograders.readthedocs.io/en/latest/specs/):

```
$ python3 -m gradescope_auto_py 'ex_assign.py'
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
  interpreter via the blank instructor copy of assignment. Student submissions
  which import a module outside of these cannot be autograded (
  see [#4](https://github.com/matthigger/gradescope_auto_py/issues/4))


- The regex to extract points is `'\d+\.?\d* pts'`:
    - any decimal point value is supported
    - parentheses in example, `(2 pts)`, are optional

## Configured asserts vs submitted asserts

The set of all assert-for-points is defined by the file passed
to `build_autograder()`. You can see them in
the [config.txt](test/ex_config.txt) included in the autograder `.zip`
produced. A submitted assignment, however, may not have the same set of
assert-for-points in the body of the code:

- If a submission is missing an assert-for-points from the configuration, it is
  appended to the end of the body of the submitted code before grading.
    - This is helpful if you wish to hide an assert-for-points from students.
- If a submission matches an assert-for-points from the configuration, it is
  run within the body of the student's submission.
    - This is helpful to allow the student to control the location of the
      assert within their submission.
- If non-matching assert-for-points appears in student copy, no points are
  awarded (though we dont yet warn student about
  it [#3](https://github.com/matthigger/gradescope_auto_py/issues/3))

## See also

- [Otter-grader](https://otter-grader.readthedocs.io/en/latest/)
- [Gradescope-utils](https://github.com/gradescope/gradescope-utils)

Be sure to check out these similar libraries to end up with the one best suited
for your needs :)