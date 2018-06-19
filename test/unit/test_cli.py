import pytest
import unittest
import logging
from unittest.mock import MagicMock, patch, call
from taskban.cli import load_parser, load_logger


class TestArgparse(unittest.TestCase):
    def setUp(self):
        self.parser = load_parser()

    def test_verbose(self):
        parsed = self.parser.parse_args(['-v', 'ocupation'])
        self.assertEqual(parsed.verbose, 1)

    def test_really_verbose(self):
        parsed = self.parser.parse_args(['-vv', 'ocupation'])
        self.assertEqual(parsed.verbose, 2)

    def test_quiet(self):
        parsed = self.parser.parse_args(['-q', 'ocupation'])
        self.assertTrue(parsed.quiet)

    def test_can_specify_taskwarrior_data_path(self):
        parsed = self.parser.parse_args(['-d', '~/task/path', 'ocupation'])
        self.assertEqual(parsed.task_data_path, '~/task/path')

    def test_ocupation_default_taskwarrior_data_path(self):
        parsed = self.parser.parse_args(['ocupation'])
        self.assertEqual(parsed.task_data_path, '~/.task/')

    def test_can_specify_taskwarrior_config_path(self):
        parsed = self.parser.parse_args(
            ['--taskrc_path', '~/task/path', 'ocupation'],
        )
        self.assertEqual(parsed.taskrc_path, '~/task/path')

    def test_ocupation_default_taskwarrior_config_path(self):
        parsed = self.parser.parse_args(['ocupation'])
        self.assertEqual(parsed.taskrc_path, '~/.taskrc')

    def test_can_specify_taskban_data_path(self):
        parsed = self.parser.parse_args(['-D', '~/task/path', 'ocupation'])
        self.assertEqual(parsed.data_path, '~/task/path')

    def test_ocupation_default_taskban_data_path(self):
        parsed = self.parser.parse_args(['ocupation'])
        self.assertEqual(parsed.data_path, '~/.local/share/taskban/')

    def test_can_specify_taskban_config_path(self):
        parsed = self.parser.parse_args(['-f', '~/task/path', 'ocupation'])
        self.assertEqual(parsed.config_path, '~/task/path')

    def test_subcommand_is_required(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args('')

    def test_has_subcommand_ocupation(self):
        parsed = self.parser.parse_args(['ocupation'])
        self.assertEqual(parsed.subcommand, 'ocupation')

    def test_ocupation_default_period(self):
        parsed = self.parser.parse_args(['ocupation'])
        self.assertEqual(parsed.period, '1d')

    def test_ocupation_can_specify_period(self):
        parsed = self.parser.parse_args(['ocupation', '-p', '2d'])
        self.assertEqual(parsed.period, '2d')

    def test_ocupation_can_specify_backlog(self):
        parsed = self.parser.parse_args(['ocupation', '-b'])
        self.assertTrue(parsed.backlog)

    def test_ocupation_backlog_not_shown_by_default(self):
        parsed = self.parser.parse_args(['ocupation'])
        self.assertFalse(parsed.backlog)

    def test_has_subcommand_snapshot(self):
        parsed = self.parser.parse_args(['snapshot'])
        self.assertEqual(parsed.subcommand, 'snapshot')

    def test_snapshot_default_period(self):
        parsed = self.parser.parse_args(['snapshot'])
        self.assertEqual(parsed.period, '100y')

    def test_snapshot_can_specify_period(self):
        parsed = self.parser.parse_args(['snapshot', '-p', '2d'])
        self.assertEqual(parsed.period, '2d')

    def test_has_subcommand_refine(self):
        parsed = self.parser.parse_args(['refine'])
        self.assertEqual(parsed.subcommand, 'refine')

    def test_refine_has_subcommand_next(self):
        parsed = self.parser.parse_args(['refine', 'next'])
        self.assertEqual(parsed.next_subcommand, 'next')

    def test_refine_has_subcommand_next_child(self):
        parsed = self.parser.parse_args(['refine', 'next', 'child'])
        self.assertEqual(parsed.parentage, 'child')

    def test_refine_has_subcommand_next_parent(self):
        parsed = self.parser.parse_args(['refine', 'next', 'parent'])
        self.assertEqual(parsed.parentage, 'parent')

    def test_refine_has_subcommand_next_sibling(self):
        parsed = self.parser.parse_args(['refine', 'next', 'sibling'])
        self.assertEqual(parsed.parentage, 'sibling')

    def test_refine_has_subcommand_prev(self):
        parsed = self.parser.parse_args(['refine', 'prev'])
        self.assertEqual(parsed.next_subcommand, 'prev')

    def test_refine_has_subcommand_prev_child(self):
        parsed = self.parser.parse_args(['refine', 'prev', 'child'])
        self.assertEqual(parsed.parentage, 'child')

    def test_refine_has_subcommand_prev_parent(self):
        parsed = self.parser.parse_args(['refine', 'prev', 'parent'])
        self.assertEqual(parsed.parentage, 'parent')

    def test_refine_has_subcommand_prev_sibling(self):
        parsed = self.parser.parse_args(['refine', 'prev', 'sibling'])
        self.assertEqual(parsed.parentage, 'sibling')

    def test_refine_has_subcommand_jump(self):
        parsed = self.parser.parse_args(['refine', 'jump', 'my-first-project'])
        self.assertEqual(parsed.next_subcommand, 'jump')
        self.assertEqual(parsed.jump_project, 'my-first-project')

    def test_has_subcommand_plan(self):
        parsed = self.parser.parse_args(['plan', '1', 'up'])
        self.assertEqual(parsed.subcommand, 'plan')

    def test_subcommand_plan_needs_direction(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['plan'])

    def test_subcommand_plan_needs_direction_and_task(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['plan', '1'])

    def test_plan_has_subcommand_move_up(self):
        parsed = self.parser.parse_args(['plan', '1', 'up'])
        self.assertEqual(parsed.plan_direction, 'up')

    def test_plan_has_subcommand_move_down(self):
        parsed = self.parser.parse_args(['plan', '1', 'down'])
        self.assertEqual(parsed.plan_direction, 'down')

    def test_plan_can_specify_pm_value(self):
        parsed = self.parser.parse_args(
            ['plan', '--task_status', 'doing', '1', 'up'],
        )
        self.assertEqual(parsed.task_status, 'doing')

    def test_plan_has_default_pm_value(self):
        parsed = self.parser.parse_args(
            ['plan', '1', 'up'],
        )
        self.assertEqual(parsed.task_status, 'todo')

    def test_plan_can_specify_project_value(self):
        parsed = self.parser.parse_args(
            ['plan', '--project', 'test', '1', 'up'],
        )
        self.assertEqual(parsed.project, 'test')

class TestLogger(unittest.TestCase):
    @patch('taskban.cli.logging')
    def test_logger_is_configured_by_default(self, logMock):
        logMock.DEBUG = 10
        logMock.INFO = 20
        logMock.WARNING = 30
        logMock.ERROR = 40
        args = MagicMock()
        args.verbose = False
        args.quiet = False
        load_logger(args)
        self.assertEqual(
            logMock.addLevelName.assert_has_calls(
                [
                    call(logging.INFO, '[\033[36m+\033[0m]'),
                    call(logging.ERROR, '[\033[31m+\033[0m]'),
                    call(logging.DEBUG, '[\033[32m+\033[0m]'),
                    call(logging.WARNING, '[\033[33m+\033[0m]'),
                ]
            ),
            None
        )
        self.assertEqual(
            logMock.basicConfig.assert_called_with(
                level=logging.WARNING,
                format="  %(levelname)s %(message)s",
            ),
            None
        )

    @patch('taskban.cli.logging')
    def test_logger_in_quiet_mode(self, logMock):
        logMock.DEBUG = 10
        logMock.INFO = 20
        logMock.WARNING = 30
        logMock.ERROR = 40
        args = MagicMock()
        args.verbose = False
        args.quiet = True
        load_logger(args)
        self.assertEqual(
            logMock.addLevelName.assert_has_calls(
                [
                    call(logging.INFO, '[\033[36m+\033[0m]'),
                    call(logging.ERROR, '[\033[31m+\033[0m]'),
                    call(logging.DEBUG, '[\033[32m+\033[0m]'),
                    call(logging.WARNING, '[\033[33m+\033[0m]'),
                ]
            ),
            None
        )
        self.assertEqual(
            logMock.basicConfig.assert_called_with(
                level=logging.ERROR,
                format="  %(levelname)s %(message)s",
            ),
            None
        )

    @patch('taskban.cli.logging')
    def test_logger_in_verbose_mode(self, logMock):
        logMock.DEBUG = 10
        logMock.INFO = 20
        logMock.WARNING = 30
        logMock.ERROR = 40
        args = MagicMock()
        args.verbose = 1
        args.quiet = False
        load_logger(args)
        self.assertEqual(
            logMock.addLevelName.assert_has_calls(
                [
                    call(logging.INFO, '[\033[36m+\033[0m]'),
                    call(logging.ERROR, '[\033[31m+\033[0m]'),
                    call(logging.DEBUG, '[\033[32m+\033[0m]'),
                    call(logging.WARNING, '[\033[33m+\033[0m]'),
                ]
            ),
            None
        )
        self.assertEqual(
            logMock.basicConfig.assert_called_with(
                level=logging.INFO,
                format="  %(levelname)s %(message)s",
            ),
            None
        )

    @patch('taskban.cli.logging')
    def test_logger_in_really_verbose_mode(self, logMock):
        logMock.DEBUG = 10
        logMock.INFO = 20
        logMock.WARNING = 30
        logMock.ERROR = 40
        args = MagicMock()
        args.verbose = 2
        args.quiet = False
        load_logger(args)
        self.assertEqual(
            logMock.addLevelName.assert_has_calls(
                [
                    call(logging.INFO, '[\033[36m+\033[0m]'),
                    call(logging.ERROR, '[\033[31m+\033[0m]'),
                    call(logging.DEBUG, '[\033[32m+\033[0m]'),
                    call(logging.WARNING, '[\033[33m+\033[0m]'),
                ]
            ),
            None
        )
        self.assertEqual(
            logMock.basicConfig.assert_called_with(
                level=logging.DEBUG,
                format="  %(levelname)s %(message)s",
            ),
            None
        )
