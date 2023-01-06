# Test case (brief) description

## HW0

hw0 has no extra files associated with it, so `include_folder=False` when the
autograder is built and no files are added to the student submission before
autograding is done:

- submit0: some answers right and wrong (no errors).  has an assert-for-points in student submission not in template (0 points) as well as assert-for-points in template not in submission (added to submission at end)
- submit1: syntax error (no points awarded, user warned)
- submit2: runtime error (points awarded before runtime error in student submission, 0 afterwards)