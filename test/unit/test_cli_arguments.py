import unittest
from taskban.cli_arguments import load_parser


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = load_parser()

    def test_verbose(self):
        parsed = self.parser.parse_args(['-v', 'now'])
        self.assertEqual(parsed.verbose, 1)

    def test_really_verbose(self):
        parsed = self.parser.parse_args(['-vv', 'now'])
        self.assertEqual(parsed.verbose, 2)

    def test_quiet(self):
        parsed = self.parser.parse_args(['-q', 'now'])
        self.assertTrue(parsed.quiet)

    def test_can_specify_taskwarrior_data_path(self):
        parsed = self.parser.parse_args(['-d', '~/task/path', 'now'])
        self.assertEqual(parsed.task_data_path, '~/task/path')

    def test_now_default_taskwarrior_data_path(self):
        parsed = self.parser.parse_args(['now'])
        self.assertEqual(parsed.task_data_path, '~/.task/')

    def test_can_specify_taskwarrior_config_path(self):
        parsed = self.parser.parse_args(['--taskrc_path', '~/task/path', 'now'])
        self.assertEqual(parsed.taskrc_path, '~/task/path')

    def test_now_default_taskwarrior_config_path(self):
        parsed = self.parser.parse_args(['now'])
        self.assertEqual(parsed.taskrc_path, '~/.taskrc')

    def test_can_specify_taskban_config_path(self):
        parsed = self.parser.parse_args(['-f', '~/task/path', 'now'])
        self.assertEqual(parsed.config_path, '~/task/path')

    def test_subcommand_is_required(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args('')

    def test_has_subcommand_now(self):
        parsed = self.parser.parse_args(['now'])
        self.assertEqual(parsed.subcommand, 'now')

    def test_now_default_period(self):
        parsed = self.parser.parse_args(['now'])
        self.assertEqual(parsed.period, '1d')

    def test_now_can_specify_period(self):
        parsed = self.parser.parse_args(['now', '-p', '2d'])
        self.assertEqual(parsed.period, '2d')

    def test_now_can_specify_backlog(self):
        parsed = self.parser.parse_args(['now', '-b'])
        self.assertTrue(parsed.backlog)

    def test_now_backlog_not_shown_by_default(self):
        parsed = self.parser.parse_args(['now'])
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
