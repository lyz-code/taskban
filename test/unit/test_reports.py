import os
import shutil
import pytest
import tasklib
import unittest
import datetime
import tempfile
from unittest.mock import patch
from taskban.reports import RefinementReport, KanbanReport, Report


class TestReport(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        shutil.rmtree(self.tmp)
        shutil.copytree('test/data', os.path.join(self.tmp, 'data'))
        shutil.copytree('test/config', os.path.join(self.tmp, 'config'))
        self.config_path = os.path.join(self.tmp, 'config')
        self.data_path = os.path.join(self.tmp, 'data')
        self.report = Report(
            task_data_path=self.data_path,
            taskrc_path=os.path.join(self.config_path, 'taskrc'),
            config_path=os.path.join(self.config_path, 'config.yaml'),
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
        actual_config = self.report.load_yaml(
            os.path.join(self.config_path, 'config.yaml'),
        )
        self.assertEqual(actual_config, desired_config)

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
            task_data_path=self.data_path,
            taskrc_path=os.path.join(self.config_path, 'taskrc'),
            config_path=os.path.join(self.config_path, 'config.yaml'),
        )

        self.assertEqual((self.report._end - self.report.start).days, 1)

    def test_start_tw_string_has_now_when_start_is_a_string(self):
        self.report = Report(
            start_date='1d',
            task_data_path=self.data_path,
            taskrc_path=os.path.join(self.config_path, 'taskrc'),
            config_path=os.path.join(self.config_path, 'config.yaml'),
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

    def test_set_start_date_of_report_type_now(self):
        self.report.start = 'now'
        self.assertIsInstance(self.report.start, type(datetime.datetime.now()))
        self.assertEqual(self.report._start_tw_string, 'now')

    def test_start_date_of_report_difference(self):
        self.report = Report(
            '1d',
            task_data_path=self.data_path,
            taskrc_path=os.path.join(self.config_path, 'taskrc'),
            config_path=os.path.join(self.config_path, 'config.yaml'),
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

    def test_save_yaml(self):
        save_file = os.path.join(self.tmp, 'yaml_save_test.yaml')
        dictionary = {'a': 'b', 'c': 'd'}
        self.report.save_yaml(save_file, dictionary)
        with open(save_file, 'r') as f:
            self.assertEqual("a: b\nc: d\n", f.read())


class TestKanbanReport(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        shutil.rmtree(self.tmp)
        shutil.copytree('test/data', os.path.join(self.tmp, 'data'))
        shutil.copytree('test/config', os.path.join(self.tmp, 'config'))
        self.config_path = os.path.join(self.tmp, 'config')
        self.data_path = os.path.join(self.tmp, 'data')
        self.report = KanbanReport(
            task_data_path=self.data_path,
            taskrc_path=os.path.join(self.config_path, 'taskrc'),
            config_path=os.path.join(self.config_path, 'config.yaml'),
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


class TestRefinementReport(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        shutil.rmtree(self.tmp)
        shutil.copytree('test/data', os.path.join(self.tmp, 'data'))
        shutil.copytree('test/config', os.path.join(self.tmp, 'config'))
        self.config_path = os.path.join(self.tmp, 'config')
        self.data_path = os.path.join(self.tmp, 'data')
        self.report = RefinementReport(
            task_data_path=self.data_path,
            taskrc_path=os.path.join(self.tmp, 'taskrc'),
            config_path=os.path.join(self.config_path, 'config.yaml'),
            data_path=self.data_path,
        )
        self.state_file = os.path.join(self.data_path, 'refinement.yaml')

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_refinement_has_state_file_attribute(self):
        self.assertEqual(self.report.state_file, self.state_file)

    @patch('taskban.reports.RefinementReport.save_yaml')
    def test_refinement_can_save_state(self, saveyamlMock):
        self.report.save()
        state = {
            'start': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M'),
            'project': '',
        }
        self.assertEqual(
            saveyamlMock.assert_called_with(self.state_file, state),
            None
        )

    @patch('taskban.reports.RefinementReport.load_yaml')
    def test_refinement_can_load_state(self, loadyamlMock):
        self.report.load()
        self.assertEqual(
            loadyamlMock.assert_called_with(self.state_file),
            None
        )
        self.assertEqual(
            str(type(self.report.state)),
            "<class 'unittest.mock.MagicMock'>",
        )

    @patch('taskban.reports.RefinementReport.load_yaml')
    def test_refinement_doesnt_error_when_absent_state_file(self, loadyamlMock):
        loadyamlMock.side_effect = FileNotFoundError
        self.report.load()


if __name__ == '__main__':
    unittest.main()
