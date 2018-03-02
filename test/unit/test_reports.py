import os
import shutil
import pytest
import tasklib
import unittest
import datetime
import tempfile
from taskban.reports import KanbanReport, Report
from taskban.cli_arguments import load_parser


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = load_parser()

    def test_verbose(self):
        parsed = self.parser.parse_args(['-v'])
        self.assertEqual(parsed.verbose, 1)

    def test_really_verbose(self):
        parsed = self.parser.parse_args(['-vv'])
        self.assertEqual(parsed.verbose, 2)

    def test_quiet(self):
        parsed = self.parser.parse_args(['-q'])
        self.assertTrue(parsed.quiet)

    def test_can_specify_taskwarrior_data_path(self):
        parsed = self.parser.parse_args(['-d', '~/task/path'])
        self.assertEqual(parsed.task_data_path, '~/task/path')

    def test_now_default_taskwarrior_data_path(self):
        parsed = self.parser.parse_args('')
        self.assertEqual(parsed.task_data_path, '~/.task/')

    def test_can_specify_taskwarrior_config_path(self):
        parsed = self.parser.parse_args(['--taskrc_path', '~/task/path'])
        self.assertEqual(parsed.taskrc_path, '~/task/path')

    def test_now_default_taskwarrior_config_path(self):
        parsed = self.parser.parse_args('')
        self.assertEqual(parsed.taskrc_path, '~/.taskrc')

    def test_can_specify_taskban_config_path(self):
        parsed = self.parser.parse_args(['-f', '~/task/path'])
        self.assertEqual(parsed.config_path, '~/task/path')

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


class TestReport(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        shutil.rmtree(self.tmp)
        shutil.copytree('test/data', self.tmp)
        self.config_path = os.path.join(self.tmp, 'config.yaml')
        self.report = Report(
            task_data_path=self.tmp,
            taskrc_path=os.path.join(self.tmp, 'taskrc'),
            config_path=self.config_path,
        )

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_report_default_config(self):
        desired_config = {
            'task_data_path': '~/.task',
            'taskrc_path': '~/.taskrc',
            'start_date': '1984-01-01',
            'max_tasks_per_state': 10,
            'available_states': {
                'todo': 'To Do',
                'doing': 'Doing',
                'done': 'Done',
                'blocked': 'Blocked',
                'test': 'Testing',
                'backlog': 'Backlog',
            },
            'states_order': [
                'done',
                'test',
                'blocked',
                'doing',
                'todo',
                'backlog',
            ],
        }
        self.report.load_config(self.config_path)
        self.assertEqual(
            self.report.config,
            desired_config,
        )

    def test_update_config_values(self):
        self.report.update_config_with_arguments(
            start_date='new_start',
            task_data_path='new_data_path',
            taskrc_path='new_taskrc_path',
            config_path='new_config_path',
        )
        self.assertEqual(self.report.config['start_date'], 'new_start')
        self.assertEqual(self.report.config['task_data_path'], 'new_data_path')
        self.assertEqual(self.report.config['taskrc_path'], 'new_taskrc_path')
        self.assertEqual(self.report.config['config_path'], 'new_config_path')

    def test_set_backend_on_initialize(self):
        self.assertIsInstance(self.report.backend, type(tasklib.TaskWarrior()))

    def test_end_date_of_report_type_datetime(self):
        self.assertIsInstance(self.report._end, type(datetime.datetime.now()))

    def test_end_date_of_report_difference(self):
        self.report = Report(
            '1d',
            task_data_path=self.tmp,
            taskrc_path=os.path.join(self.tmp, 'taskrc'),
            config_path=self.config_path,
        )

        self.assertEqual((self.report._end - self.report.start).days, 1)

    def test_start_tw_string_has_now_when_start_is_a_string(self):
        self.report = Report(
            start_date='1d',
            task_data_path=self.tmp,
            taskrc_path=os.path.join(self.tmp, 'taskrc'),
            config_path=self.config_path,
        )
        self.assertEqual(
            self.report._start_tw_string,
            'now - 1d',
        )

    def test_set_start_date_of_report_type_difference(self):
        self.report.start = '1d'
        self.assertIsInstance(self.report.start, type(datetime.datetime.now()))

    def test_set_start_date_of_report_type_date(self):
        self.report.start = '1984-01-01'
        self.assertEqual(
            self.report.start,
            self.report.backend.convert_datetime_string('1984-01-01')
        )

    def test_start_date_of_report_difference(self):
        self.report = Report(
            '1d',
            task_data_path=self.tmp,
            taskrc_path=os.path.join(self.tmp, 'taskrc'),
            config_path=self.config_path,
        )
        self.assertEqual(
            self.report._end - self.report.start,
            datetime.timedelta(1),
        )

    def test_report_has_history(self):
        self.assertIsInstance(self.report.backend.history.entries, list)

    def test_report_report_has_title(self):
        self.assertIsInstance(self.report.title, str)

    def test_report_report_has_content(self):
        self.assertIsInstance(self.report.content, dict)

    def test_report_convert_seconds_to_readable(self):
        self.assertEqual(self.report.seconds_to_readable(6162), '01:42:42')


class TestKanbanReport(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        shutil.rmtree(self.tmp)
        shutil.copytree('test/data', self.tmp)
        self.report = KanbanReport(
            task_data_path=self.tmp,
            taskrc_path=os.path.join(self.tmp, 'taskrc'),
            config_path=os.path.join(self.tmp, 'config.yaml'),
        )

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_report_has_kanban_states(self):
        self.assertIsInstance(self.report.config['available_states'], dict)

    def test_report_has_kanban_states_order(self):
        self.assertIsInstance(self.report.config['states_order'], list)

    def test_all_available_tests_are_ordered(self):
        self.assertEqual(set(self.report.config['available_states'].keys()),
                         set(self.report.config['states_order']))

    def test_report_has_max_tasks_per_state(self):
        self.assertEqual(self.report.config['max_tasks_per_state'], 10)

    def test_report_can_get_tasks_of_state_backlog(self):
        tasks = self.report._get_tasks_of_state('backlog')
        self.assertTrue(str(tasks[0]) == 'Backlog task 1')
        self.assertTrue(str(tasks[1]) == 'Backlog task 2')
        self.assertTrue(str(tasks[2]) == 'Backlog task 3')

    def test_report_can_get_tasks_of_state_done(self):
        tasks = self.report._get_tasks_of_state('done')
        self.assertTrue(str(tasks[0]) == 'Done task 1')

    def test_report_can_make_snapshot(self):
        self.assertTrue(
            str(self.report.snapshot['test']['my-second-project'][0]),
            'Testing task 1',
        )
        self.assertTrue(
            str(self.report.snapshot['todo']['my-first-project'][0]),
            'Todo task 3',
        )
        self.assertTrue(
            str(self.report.snapshot['doing']['my-second-project'][0]),
            'Doing task 2',
        )
        self.assertTrue(
            str(self.report.snapshot['backlog']['my-second-project'][0]),
            'Backlog task 3',
        )

    # @pytest.mark.skip(
    #     reason="difficult to test prints, I leave the work started in case"
    #     "anyone wants to continue")
    # def test_report_can_print_report(self):
    #     from io import StringIO
    #     out = StringIO()
    #     self.report.print_report(out=out)
    #     output = out.getvalue().strip()
    #     with open('test/data/taskban_report_sample', 'r') as f:
    #         self.assertEqual(output, f.read())

    @pytest.mark.skip()
    def test_skip(self):
        pass


if __name__ == '__main__':
    unittest.main()
