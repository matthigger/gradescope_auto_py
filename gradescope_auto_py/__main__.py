#!/usr/bin/env python3

import argparse
import json
import sys

import gradescope_auto_py as gap


def parse_args(args):
    parser = argparse.ArgumentParser(
        description='auto grader python code in gradescope (see doc at: '
                    'https://github.com/matthigger/gradescope_auto_py/)')
    parser.add_argument('f_template', type=str,
                        help='assignment template (defines pts per assert)')
    parser.add_argument('--run', dest='file_run', action='store', default=None,
                        help='name of submitted file to run (there may be '
                             'many submitted files).  defaults to same name '
                             'as template file.')
    parser.add_argument('--supplement', dest='include_folder',
                        action='store_true',
                        help='includes all files in folder which holds '
                             'the template file.  these supplementary files '
                             'will be copied alongside student submission '
                             'while autograding (overwriting if need be).  '
                             'zip files may not be supplementary')
    parser.add_argument('--submit', dest='f_submit', action='store',
                        default=None,
                        help='student copy of assignment.  if passed json '
                             'scoring is produced')
    return parser.parse_args(args)


def main(args):
    """ builds zip from f_template, if passed gets json of submission

    Args:
        args: has attributes f_assign and f_submit (see parse_args() above)

    """
    # build zip
    gap.build_autograder(file_template=args.f_template,
                         include_folder=args.include_folder,
                         file_run=args.file_run)

    # autograde if need be
    if args.f_submit is not None:
        grader_config = gap.GraderConfig.from_py(args.f_template)
        grader = gap.Grader(grader_config.afp_list)
        grader.grade(args.f_submit)

        f_json = args.f_submit.replace('.py', '_out.json')
        with open(f_json, 'w') as f:
            json.dump(grader.get_json(), f, indent=4, sort_keys=True)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    main(args)
