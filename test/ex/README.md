# Test case (brief) description

## HW0 `build_autograder(file_template, include_folder=False)`

hw0 has no supplementary files associated with it.

- submit0: some answers right and wrong (no errors). has an assert-for-points
  in student submission not in template (0 points) as well as assert-for-points
  in template not in submission (added to submission at end)
- submit1: syntax error (no points awarded, user warned)
- submit2: runtime error (points awarded before runtime error in student
  submission, 0 afterwards)

## HW1 `build_autograder(file_template, include_folder=True)`

hw1 has supplementary files that are to be included alongside student
submission when run.

- submit0: contains only the student's submission
- submit1: contains copies of supplementary files (will be overwritten & warning given)
- submit2: doesn't contain file_run (throw warning to student, no points awarded)