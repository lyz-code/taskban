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
