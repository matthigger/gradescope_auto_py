# Gradescope Autograder for Python

## Installation

    $ pip install gradescope_auto_py

## Method

1. associate point values to `assert` statements in a blank copy of assignment 
   1. we call these "assert-for-points"
2. students leave these assert-for-points unmodified as they write software in the assignment
3. gradescope automatically gives points for passing assert-for-points in submitted code

## Usage

1. Define assert-for-points by adding a point value to any `assert` statements in a blank copy of the assignment (
   e.g. [ex_assign.py](test/ex_assign_pretty.py))

```python
assert get_area(radius=1) == pi, 'case0: area from r=1 (2 pts)'
```

2. [build_autograder()](gradescope_auto_py/gradescope/build_auto.py) builds
   a `.zip` next from this blank copy of the assignment:

```python
import gradescope_auto_py as gap

# generate hw0.zip in same folder as hw0.py
gap.build_autograder('hw0.py')
```

This zip follows [gradescope's autograder format](https://gradescope-autograders.readthedocs.io/en/latest/specs/) and can be uploaded to any gradescope "programming assignment".

## Notes

- the assert-for-points are defined by the instructor copy of the
  assignment (and encapsulated in [config.txt](test/ex_config.txt)) though only the assert statements in a student submission are run
    - if assert-for-points in instructor copy is not present in student submission then no points awarded
    - (not yet [#3](https://github.com/matthigger/gradescope_auto_py/issues/3)) if assert-for-points in student submission doesn't match one in the instructor copy, a warning is thrown to the student and no points are awarded 
    - because of this, it is not possible to "hide" any asserts from the student (see [#1](https://github.com/matthigger/gradescope_auto_py/issues/1))


- We automatically identify the modules to be installed on gradescope's
  interpreter via the blank instructor copy of assignment. Student submissions
  which import a module outside of these cannot be autograded (
  see [#4](https://github.com/matthigger/gradescope_auto_py/issues/4))


- The regex to extract points is `'\d+\.?\d* pts'`:
    - any decimal point value is supported
    - parentheses in example, `(2 pts)`, are optional

## See also

- [Otter-grader](https://otter-grader.readthedocs.io/en/latest/)
- [Gradescope-utils](https://github.com/gradescope/gradescope-utils)

Be sure to check out these similar libraries to end up with the one best suited
for your needs :)