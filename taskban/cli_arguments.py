import os
import sys
import yaml
import logging
import argparse
import argcomplete


def load_parser():
    ''' Configure environment '''

    # Argparse
    parser = argparse.ArgumentParser(
        description=" Implement my Kanban workflow with Taskwarrior")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-q", "--quiet", action="store_true")

    subparser = parser.add_subparsers(dest='subcommand', help='subcommands')
    now_parser = subparser.add_parser('now')
    snapshot_parser = subparser.add_parser('snapshot')

    parser.add_argument("-d", "--data", type=str, default='~/.task/',
                        help='Taskwarrior data directory path')

    now_parser.add_argument("-p", "--period", type=str, default='1d',
                            help='Taskwarrior compatible date string')
    now_parser.add_argument("-b", "--backlog", action="store_true",
                            help="Show backlog")
    snapshot_parser.add_argument("-p", "--period", type=str, default='100y',
                                 help='Taskwarrior compatible date string')
    # now_parser.add_argument("main_argument", type=str, help='')
    # parser.add_argument("--optional_argument", nargs='?', type=str, help='')
    # parser.add_argument("--optional_argument_choices", nargs='?',
    #                     type=str, choices=['0', '1'], help='')
    # parser.add_argument("-f", "--rc_file", nargs='?',
    #                     default='~/." + main_file_name + "rc', type=str,
    #                     help='Use selected configuration file')
    argcomplete.autocomplete(parser)
    return parser


def load_config(log):
    try:
        config_file = os.path.expanduser("~/.config/taskban/taskban.yml")
        with open(config_file, 'r') as f:
            try:
                config = yaml.safe_load(f)
            except yaml.YAMLError as e:
                log.error(e)
                sys.exit(1)
            return config
    except FileNotFoundError as e:
        log.warning('Error opening config file {}'.format(config_file))


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
    return logging.getLogger('Main')
