from enum import Enum


class Visibility(Enum):
    """ controls visibility of a test case

    https://gradescope-autograders.readthedocs.io/en/latest/specs/#controlling-test-case-visibility

    visible (default): test case will always be shown
    hidden: test case will never be shown to students
    after_due_date: test case will be shown after the assignment's due date has passed. If late submission is allowed, then test will be shown only after the late due date.
    after_published: test case will be shown only when the assignment is explicitly published from the "Review Grades" page
    """
    VISIBLE = 'visible'
    HIDDEN = 'hidden'
    AFTER_DUE_DATE = 'after_due_date'
    AFTER_PUBLISHED = 'after_published'

    @classmethod
    def parse(cls, s):
        """finds unique visibility setting, returns None if not found

        Args:
            s (str): input string containing values of each state (e.g.
                'visible')

        Returns:
            viz (Visibility): unique visibility setting
        """
        # parse
        match_list = list()
        for x in cls:
            if x.value in s:
                match_list.append(x)

        if len(match_list) > 1:
            raise RuntimeError(f'no unique viz found in {s}: {match_list}')

        if not match_list:
            # no matches found
            return None

        # unique match found
        return match_list[0]
