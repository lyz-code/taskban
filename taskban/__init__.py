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

from taskban.reports import KanbanReport
from taskban.cli import load_logger, load_parser


def main():
    parser = load_parser()
    args = parser.parse_args()
    load_logger(args)

    if args.subcommand == 'ocupation':
        report = KanbanReport(
            start_date=args.period,
            task_data_path=args.task_data_path,
            taskrc_path=args.taskrc_path,
            config_path=args.config_path,
        )
        report.print_report(
            show_backlog=args.backlog,
            show_inactive=args.inactive
        )


if __name__ == "__main__":
    main()
