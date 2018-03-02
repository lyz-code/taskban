import logging
import argparse
import argcomplete


def load_parser():
    ''' Configure environment '''

    # Argparse
    parser = argparse.ArgumentParser(
        description=" Implement my Kanban workflow with Taskwarrior")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="count")
    group.add_argument("-q", "--quiet", action="store_true")

    subparser = parser.add_subparsers(dest='subcommand', help='subcommands')
    now_parser = subparser.add_parser('now')
    snapshot_parser = subparser.add_parser('snapshot')

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
        help='Taskwarrior data directory path',
    )

    parser.add_argument(
        "-f",
        "--config_path",
        type=str,
        default='~/.local/share/taskban/config.yaml',
        help='Taskwarrior data directory path',
    )

    now_parser.add_argument("-p", "--period", type=str, default='1d',
                            help='Taskwarrior compatible date string')
    now_parser.add_argument("-b", "--backlog", action="store_true",
                            help="Show backlog")
    snapshot_parser.add_argument("-p", "--period", type=str, default='100y',
                                 help='Taskwarrior compatible date string')
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
