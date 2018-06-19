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
from taskban.reports import KanbanReport, RefinementReport, PlanningReport
from taskban.cli import load_logger, load_parser


def _refinement_next_parent(report, direction):
    try:
        report.next('parent', direction)
    except IndexError:
        if direction == 1:
            print('There are no more projects :)')
            report.end()
        else:
            print('You are on the first project')


def _refinement_next_child(report, direction):
    try:
        report.next('child', direction)
    except IndexError:
        print('There are no more children')


def refinement_next_project(args, report, direction):
    if args.parentage == 'parent':
        _refinement_next_parent(report, direction)
    elif args.parentage == 'child':
        _refinement_next_child(report, direction)
    elif args.parentage == 'sibling':
        try:
            report.next('sibling', direction)
        except IndexError:
            print('There are no more children')
    else:
        try:
            report.next('child', direction)
        except IndexError:
            try:
                report.next('sibling', direction)
            except IndexError:
                _refinement_next_parent(report, direction)


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
    elif args.subcommand == 'refine':
        report = RefinementReport(
            task_data_path=args.task_data_path,
            taskrc_path=args.taskrc_path,
            config_path=args.config_path,
            data_path=args.data_path,
        )

        if args.next_subcommand == 'jump':
            report.jump(args.jump_project)
        elif args.next_subcommand == 'next':
            direction = 1
            refinement_next_project(args, report, direction)
        elif args.next_subcommand == 'prev':
            direction = -1
            refinement_next_project(args, report, direction)
        else:
            os.system('task rc:{} pro:{} list'.format(
                    args.taskrc_path,
                    report.state['project'],
                ),
            )
    elif args.subcommand == 'plan':
        report = PlanningReport(
            task_data_path=args.task_data_path,
            taskrc_path=args.taskrc_path,
            config_path=args.config_path,
            data_path=args.data_path,
            task_state=args.task_status,
            project=args.project,
        )
        if args.plan_direction == 'up':
            report.move_up(args.task_id)
        elif args.plan_direction == 'down':
            report.move_down(args.task_id)


if __name__ == "__main__":
    main()
