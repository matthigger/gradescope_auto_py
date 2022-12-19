#!/usr/bin/env python3

import argparse
import json
import sys

import gradescope_auto_py as gap


def parse_args(args):
    parser = argparse.ArgumentParser(
        description='auto grader python code in gradescope (see doc at: '
                    'https://github.com/matthigger/gradescope_auto_py/)')
    parser.add_argument('f_assign', type=str,
                        help='teacher copy of assignment (defines pts per assert)')
    parser.add_argument('--submit', dest='f_submit', action='store',
                        default=None,
                        help='student copy of assignment.  if passed json '
                             'scoring is produced')
    return parser.parse_args(args)


def main(args):
    """ builds zip from f_assign, if passed gets json of submission

    Args:
        args: has attributes f_assign and f_submit (see parse_args() above)

    """
    # build zip
    gap.build_autograder(file_assign=args.f_assign)

    # autograde if need be
    if args.f_submit is not None:
        grader_config = gap.GraderConfig.from_py(args.f_assign)
        grader = gap.Grader(grader_config)
        grader.grade(args.f_submit)

        f_json = args.f_submit.replace('.py', '_out.json')
        with open(f_json, 'w') as f:
            json.dump(grader.get_json(), f, indent=4, sort_keys=True)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    main(args)
