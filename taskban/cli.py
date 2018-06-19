import logging
import argparse
import argcomplete


def load_parser():
    ''' Configure environment '''

    # Argparse
    parser = argparse.ArgumentParser(
        description=" Implement my Kanban workflow with Taskwarrior",
    )

    parser.add_argument(
        "-d",
        "--task_data_path",
        type=str,
        default='~/.task/',
        help='Taskwarrior data directory path',
    )

    parser.add_argument(
        "--taskrc_path",
        type=str,
        default='~/.taskrc',
        help='Taskwarrior config file path',
    )

    parser.add_argument(
        "-f",
        "--config_path",
        type=str,
        default='~/.local/share/taskban/config.yaml',
        help='Taskban data directory path',
    )

    parser.add_argument(
        "-D",
        "--data_path",
        type=str,
        default='~/.local/share/taskban/',
        help='Taskban data directory path',
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="count")
    group.add_argument("-q", "--quiet", action="store_true")

    subparser = parser.add_subparsers(dest='subcommand', help='subcommands')
    subparser.required = True

    ocupation_parser = subparser.add_parser('ocupation')
    ocupation_parser.add_argument(
        "-p",
        "--period",
        type=str,
        default='1d',
        help='Taskwarrior compatible date string',
    )
    ocupation_parser.add_argument(
        "-b",
        "--backlog",
        action="store_true",
        help="Show backlog",
    )
    ocupation_parser.add_argument(
        "-i",
        "--inactive",
        action="store_true",
        help="Show inactive tasks",
    )

    snapshot_parser = subparser.add_parser('snapshot')
    snapshot_parser.add_argument(
        "-p",
        "--period",
        type=str,
        default='100y',
        help='Taskwarrior compatible date string',
    )

    refine_parser = subparser.add_parser('refine')
    refine_next_subparser = refine_parser.add_subparsers(
        dest='next_subcommand',
        help='Next project subparser',
    )
    refine_next_parser = refine_next_subparser.add_parser('next')
    refine_next_parser.add_argument(
        'parentage',
        choices=['child', 'parent', 'sibling'],
        help='Navigate to the next child/parent/sibling',
        nargs='?',
    )

    refine_prev_parser = refine_next_subparser.add_parser('prev')
    refine_prev_parser.add_argument(
        'parentage',
        choices=['child', 'parent', 'sibling'],
        help='Navigate to the previous child/parent/sibling',
        nargs='?',
    )
    refine_jump_parser = refine_next_subparser.add_parser('jump')
    refine_jump_parser.add_argument(
        'jump_project',
        type=str,
        help='Jump to a specific project',
        metavar='project',
    )

    plan_parser = subparser.add_parser('plan')
    plan_parser.add_argument(
        'task_id',
        type=int,
        help='Taskwarrior task ID',
    )
    plan_parser.add_argument(
        'plan_direction',
        choices=['up', 'down'],
        help='Direction to move the task',
        metavar='direction',
    )

    argcomplete.autocomplete(parser)
    return parser


def load_logger(args):
    logging.addLevelName(logging.INFO, "[\033[36m+\033[0m]")
    logging.addLevelName(logging.ERROR, "[\033[31m+\033[0m]")
    logging.addLevelName(logging.DEBUG, "[\033[32m+\033[0m]")
    logging.addLevelName(logging.WARNING, "[\033[33m+\033[0m]")
    if args.verbose is 1:
        logging.basicConfig(level=logging.INFO,
                            format="  %(levelname)s %(message)s")
    elif args.verbose is 2:
        logging.basicConfig(level=logging.DEBUG,
                            format="  %(levelname)s %(message)s")
    elif args.quiet:
        logging.basicConfig(level=logging.ERROR,
                            format="  %(levelname)s %(message)s")
    else:
        logging.basicConfig(level=logging.WARNING,
                            format="  %(levelname)s %(message)s")
    # return logging.getLogger('Main')
