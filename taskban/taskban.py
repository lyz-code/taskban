#!/usr/bin/python
# taskban: Implement my Kanban workflow with Taskwarrior
#
# Copyright (C) 2017 Lyz <lyz@riseup.net>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import os
import sys
import yaml
import logging
import argparse


def config_env(argv):
    ''' Configure environment '''

    # Argparse
    global args
    parser = argparse.ArgumentParser(
        description=" Implement my Kanban workflow with Taskwarrior")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-q", "--quiet", action="store_true")

    parser.add_argument("main_argument", type=str, help='')
    parser.add_argument("--optional_argument", nargs='?', type=str, help='')
    parser.add_argument("--optional_argument_choices", nargs='?',
                        type=str, choices=['0', '1'], help='')
    parser.add_argument("-f", "--rc_file", nargs='?',
                        default='~/." + main_file_name + "rc', type=str,
                        help='Use selected configuration file')
    args = parser.parse_args()

    # Yaml
    global config
    with open("config.yaml", 'r') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            log.error(e)
            sys.exit(1)
        global config

    # Logging
    global log
    logging.addLevelName(logging.ERROR, "[[31m+[0m]")
    logging.addLevelName(logging.DEBUG, "[[32m+[0m]")
    logging.addLevelName(logging.WARNING, "[[33m+[0m]")
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG,
                            format="  %(levelname)s %(message)s")
    elif args.quiet:
        logging.basicConfig(level=logging.ERROR,
                            format="  %(levelname)s %(message)s")
    else:
        logging.basicConfig(level=logging.WARNING,
                            format="  %(levelname)s %(message)s")
    log = logging.getLogger('Main')
    

def main(argv):
    config_env(argv)

if __name__ == "__main__":
    main(sys.argv)