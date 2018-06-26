import os
import shutil
import pytest
import tasklib
import unittest
import datetime
import tempfile
from unittest.mock import patch
from taskban.reports import PlanningReport, RefinementReport, KanbanReport, \
    Report


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
            'minimum_ord_step': 0.1,
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
            taskrc_path=os.path.join(self.config_path, 'taskrc'),
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
            'project': 'my-first-project',
        }
        self.assertEqual(
            saveyamlMock.assert_called_with(self.state_file, state),
            None
        )

    @patch('taskban.reports.RefinementReport.load_yaml')
    def test_refinement_can_load_state(self, loadyamlMock):
        self.report.load()
        self.assertEqual(
            loadyamlMock.assert_called_with(self.state_file, no_fail=True),
            None,
        )
        self.assertEqual(
            str(type(self.report.state)),
            "<class 'unittest.mock.MagicMock'>",
        )

    @patch('taskban.reports.RefinementReport.load_yaml')
    def test_refinement_absent_state_file_instate_new_report(
        self,
        loadyamlMock,
    ):
        loadyamlMock.side_effect = FileNotFoundError
        state = {
            'start': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M'),
            'project': 'my-first-project',
        }

        self.report.load()
        self.assertEqual(self.report.state, state)

    @patch('taskban.reports.os')
    def test_refinement_has_end_method(self, osMock):
        self.report.end()
        self.assertEqual(
            osMock.remove.assert_called_with(self.state_file),
            None,
        )

    @patch('taskban.reports.os')
    def test_refinement_prints_report_when_no_project_is_set(self, osMock):
        self.report.print_report()
        self.assertEqual(
            osMock.system.assert_called_with(
                'TASKDATA={} task rc:{} project:my-first-project list'.format(
                    self.data_path,
                    os.path.join(self.config_path, 'taskrc'),
                ),
            ),
            None,
        )

    def test_refinement_can_find_project_position_on_projects(self):
        self.assertEqual(
            self.report.find_project_position('my-first-project'),
            [0, 0, 0],
        )
        self.assertEqual(
            self.report.find_project_position('my-second-project'),
            [1, 0, 0],
        )

    def test_refinement_can_find_project_position_on_subprojects(self):
        self.assertEqual(
            self.report.find_project_position(
                'my-first-project.my-first-subproject',
            ),
            [0, 1, 0],
        )
        self.assertEqual(
            self.report.find_project_position(
                'my-first-project.my-second-subproject',
            ),
            [0, 2, 0],
        )

    def test_refinement_can_find_project_position_on_subsubprojects(self):
        self.assertEqual(
            self.report.find_project_position(
                'my-first-project.my-first-subproject.my-first-subsubproject',
            ),
            [0, 1, 1],
        )
        self.assertEqual(
            self.report.find_project_position(
                'my-first-project.my-first-subproject.my-second-subsubproject',
            ),
            [0, 1, 2],
        )

    def test_refinement_find_project_position_raise_on_error(self):
        with self.assertRaises(KeyError):
            self.report.find_project_position('unexisting-project')

    def test_refinement_can_find_project_on_projects(self):
        self.assertEqual(
            self.report.find_project([0, 0, 0]),
            'my-first-project',
        )
        self.assertEqual(
            self.report.find_project([1, 0, 0]),
            'my-second-project',
        )

    def test_refinement_can_find_project_on_subprojects(self):
        self.assertEqual(
            self.report.find_project([0, 1, 0]),
            'my-first-project.my-first-subproject',
        )
        self.assertEqual(
            self.report.find_project([0, 2, 0]),
            'my-first-project.my-second-subproject',
        )

    def test_refinement_can_find_project_on_subsubprojects(self):
        self.assertEqual(
            self.report.find_project([0, 1, 1]),
            'my-first-project.my-first-subproject.my-first-subsubproject',
        )
        self.assertEqual(
            self.report.find_project([0, 1, 2]),
            'my-first-project.my-first-subproject.my-second-subsubproject',
        )

    @patch('taskban.reports.RefinementReport.save')
    def test_refinement_can_set_next_sibling_on_projects(self, saveMock):
        self.report.next('sibling')
        self.assertEqual(self.report.state['project'], 'my-second-project')
        self.assertTrue(saveMock.called)

    @patch('taskban.reports.RefinementReport.save')
    def test_refinement_can_set_next_sibling_on_subprojects(self, saveMock):
        self.report.state['project'] = 'my-first-project.my-first-subproject'
        self.report.next('sibling')
        self.assertEqual(
            self.report.state['project'],
            'my-first-project.my-second-subproject',
        )
        self.assertTrue(saveMock.called)

    @patch('taskban.reports.RefinementReport.save')
    def test_refinement_can_set_next_sibling_on_subsubprojects(self, saveMock):
        self.report.state['project'] = \
            'my-first-project.my-first-subproject.my-first-subsubproject'
        self.report.next('sibling')
        self.assertEqual(
            self.report.state['project'],
            'my-first-project.my-first-subproject.my-second-subsubproject',
        )
        self.assertTrue(saveMock.called)

    @patch('taskban.reports.RefinementReport.save')
    def test_refinement_can_set_next_child_on_projects(self, saveMock):
        self.report.next('child')
        self.assertEqual(
            self.report.state['project'],
            'my-first-project.my-first-subproject',
        )
        self.assertTrue(saveMock.called)

    @patch('taskban.reports.RefinementReport.save')
    def test_refinement_can_set_next_child_on_subprojects(self, saveMock):
        self.report.state['project'] = 'my-first-project.my-first-subproject'
        self.report.next('child')
        self.assertEqual(
            self.report.state['project'],
            'my-first-project.my-first-subproject.my-first-subsubproject',
        )
        self.assertTrue(saveMock.called)

    @patch('taskban.reports.RefinementReport.save')
    def test_refinement_cant_set_next_child_on_subsubprojects(self, saveMock):
        self.report.state['project'] = \
            'my-first-project.my-first-subproject.my-first-subsubproject'
        with self.assertRaises(IndexError):
            self.report.next('child')
        self.assertFalse(saveMock.called)

    @patch('taskban.reports.RefinementReport.save')
    def test_refinement_cant_set_next_parent_on_projects(self, saveMock):
        self.report.state['project'] = 'my-first-project'
        with self.assertRaises(IndexError):
            self.report.next('parent')
        self.assertFalse(saveMock.called)

    @patch('taskban.reports.RefinementReport.save')
    def test_refinement_can_set_next_parent_on_subprojects(self, saveMock):
        self.report.state['project'] = 'my-first-project.my-first-subproject'
        self.report.next('parent')
        self.assertEqual(self.report.state['project'], 'my-second-project')
        self.assertTrue(saveMock.called)

    @patch('taskban.reports.RefinementReport.save')
    def test_refinement_can_set_next_parent_on_subsubprojects(self, saveMock):
        self.report.state['project'] = \
            'my-first-project.my-first-subproject.my-first-subsubproject'
        self.report.next('parent')
        self.assertEqual(
            self.report.state['project'],
            'my-first-project.my-second-subproject',
        )
        self.assertTrue(saveMock.called)

    @patch('taskban.reports.RefinementReport.save')
    def test_refinement_can_set_previous_sibling_on_projects(self, saveMock):
        self.report.state['project'] = 'my-second-project'
        self.report.next('sibling', direction=-1)
        self.assertEqual(self.report.state['project'], 'my-first-project')
        self.assertTrue(saveMock.called)

    @patch('taskban.reports.RefinementReport.save')
    def test_refinement_can_set_previous_sibling_on_subprojects(self, saveMock):
        self.report.state['project'] = 'my-first-project.my-second-subproject'
        self.report.next('sibling', direction=-1)
        self.assertEqual(
            self.report.state['project'],
            'my-first-project.my-first-subproject',
        )
        self.assertTrue(saveMock.called)

    @patch('taskban.reports.RefinementReport.save')
    def test_refinement_can_set_previous_sibling_on_subsubprojects(
        self,
        saveMock
    ):
        self.report.state['project'] = \
            'my-first-project.my-first-subproject.my-second-subsubproject'
        self.report.next('sibling', direction=-1)
        self.assertEqual(
            self.report.state['project'],
            'my-first-project.my-first-subproject.my-first-subsubproject',
        )
        self.assertTrue(saveMock.called)

    @patch('taskban.reports.RefinementReport.save')
    def test_refinement_can_set_previous_child_on_projects(self, saveMock):
        self.report.state['project'] = 'my-second-project'
        self.report.next('child', direction=-1)
        self.assertEqual(
            self.report.state['project'],
            'my-first-project.my-first-subproject',
        )
        self.assertTrue(saveMock.called)

    @patch('taskban.reports.RefinementReport.save')
    def test_refinement_can_set_previous_child_on_subprojects(self, saveMock):
        self.report.state['project'] = 'my-first-project.my-second-subproject'
        self.report.next('child', direction=-1)
        self.assertEqual(
            self.report.state['project'],
            'my-first-project.my-first-subproject.my-first-subsubproject',
        )
        self.assertTrue(saveMock.called)

    @patch('taskban.reports.RefinementReport.save')
    def test_refinement_cant_set_previous_child_on_subsubprojects(
        self,
        saveMock,
    ):
        self.report.state['project'] = \
            'my-first-project.my-first-subproject.my-first-subsubproject'
        with self.assertRaises(IndexError):
            self.report.next('child', direction=-1)
        self.assertFalse(saveMock.called)

    @patch('taskban.reports.RefinementReport.save')
    def test_refinement_cant_set_previous_parent_on_projects(self, saveMock):
        self.report.state['project'] = 'my-first-project'
        with self.assertRaises(IndexError):
            self.report.next('parent', direction=-1)
        self.assertFalse(saveMock.called)

    @patch('taskban.reports.RefinementReport.save')
    def test_refinement_can_set_previous_parent_on_subprojects(self, saveMock):
        self.report.state['project'] = 'my-first-project.my-first-subproject'
        self.report.next('parent', direction=-1)
        self.assertEqual(self.report.state['project'], 'my-first-project')
        self.assertTrue(saveMock.called)

    @patch('taskban.reports.RefinementReport.save')
    def test_refinement_can_set_previous_parent_on_subsubprojects(
        self,
        saveMock,
    ):
        self.report.state['project'] = \
            'my-first-project.my-first-subproject.my-first-subsubproject'
        self.report.next('parent', direction=-1)
        self.assertEqual(
            self.report.state['project'],
            'my-first-project.my-first-subproject',
        )
        self.assertTrue(saveMock.called)

    @patch('taskban.reports.RefinementReport.save')
    def test_refinement_can_jump_to_project(self, saveMock):
        self.report.jump(
            'my-first-project.my-first-subproject.my-first-subsubproject',
        )
        self.assertEqual(
            self.report.state['project'],
            'my-first-project.my-first-subproject.my-first-subsubproject',
        )
        self.assertTrue(saveMock.called)

    @patch('taskban.reports.RefinementReport.save')
    def test_refinement_cant_jump_to_unexisting_project(self, saveMock):
        with self.assertRaises(KeyError):
            self.report.jump('unexisting-project')
        self.assertFalse(saveMock.called)


class TestPlanningReport(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        shutil.rmtree(self.tmp)
        shutil.copytree('test/data', os.path.join(self.tmp, 'data'))
        shutil.copytree('test/config', os.path.join(self.tmp, 'config'))
        self.config_path = os.path.join(self.tmp, 'config')
        self.data_path = os.path.join(self.tmp, 'data')
        self.report = PlanningReport(
            task_data_path=self.data_path,
            taskrc_path=os.path.join(self.config_path, 'taskrc'),
            config_path=os.path.join(self.config_path, 'config.yaml'),
            data_path=self.data_path,
        )
        self.state_file = os.path.join(self.data_path, 'refinement.yaml')

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_plan_can_get_affected_tasks(self):
        self.report.get_affected_tasks('backlog', 'my-first-project')
        self.assertEqual(len(self.report.tasks), 6)
        self.assertEqual(self.report.tasks[0]['description'], 'Backlog task 1')

    def test_plan_gets_todo_affected_tasks_by_default(self):
        self.report.get_affected_tasks()
        self.assertEqual(len(self.report.tasks), 3)
        self.assertEqual(self.report.tasks[0]['description'], 'Todo task 3')

    def test_plan_gets_affected_tasks_can_filter_by_pm_only(self):
        self.report.get_affected_tasks('doing')
        self.assertEqual(len(self.report.tasks), 2)
        self.assertEqual(self.report.tasks[0]['description'], 'Doing task 1')

    def test_plan_can_get_task_position(self):
        self.assertEqual(self.report._get_task_position(6), 2)

    def test_plan_can_increase_ord_of_a_task_without_ord(self):
        self.report._increase_task_ord(4, 0.1)
        task = self.report.backend.tasks.get(id=4)
        self.assertEqual(task['ord'], 0.1)

    def test_plan_can_increase_ord_of_a_task_with_ord(self):
        self.report.get_affected_tasks('backlog')
        self.report._increase_task_ord(1, 0.1)
        task = self.report.backend.tasks.get(id=1)
        self.assertEqual(task['ord'], 3.1)

    def test_plan_increase_ord_of_a_task_edits_the_taskrc(self):
        self.report.get_affected_tasks('backlog')
        self.report._increase_task_ord(1, 0.6)
        task = self.report.backend.tasks.get(id=1)
        self.assertEqual(task['ord'], 3.6)
        with open(self.report.backend.taskrc_location, 'r') as f:
            config_content = f.read().splitlines()
            self.assertIn(
                "urgency.uda.ord.0.6.coefficient=0.6",
                config_content,
            )
            self.assertIn(
                "urgency.uda.ord.0.600000.coefficient=0.6",
                config_content,
            )

    def test_plan_can_move_task_up_with_enough_space(self):
        self.report.get_affected_tasks('backlog')
        self.report.move_task_up(3)
        task = self.report.backend.tasks.get(id=3)
        self.assertEqual(task['ord'], 2.5)
        self.assertEqual(round(task['urgency'], 3), 3.5)

    def test_plan_can_move_task_up_without_two_tasks_above_it_half_step(self):
        self.report.get_affected_tasks('backlog')
        self.report.move_task_up(2)
        task = self.report.backend.tasks.get(id=2)
        self.assertEqual(task['ord'], 3.5)
        self.assertEqual(round(task['urgency'], 3), 4.5)

    def test_plan_move_up_does_nothing_if_on_top(self):
        self.report.get_affected_tasks('backlog')
        self.report.move_task_up(1)
        task = self.report.backend.tasks.get(id=1)
        self.assertEqual(task['ord'], 3)
        self.assertEqual(round(task['urgency'], 3), 4)

    def test_plan_move_up_pads_tasks_above_if_there_is_no_space(self):
        self.report.move_task_up(6)
        task1 = self.report.backend.tasks.get(id=4)
        task2 = self.report.backend.tasks.get(id=5)
        task3 = self.report.backend.tasks.get(id=6)
        self.assertEqual(task1['ord'], 0.2)
        self.assertEqual(round(task1['urgency'], 3), 1.2)
        self.assertEqual(task2['ord'], None)
        self.assertEqual(round(task2['urgency'], 3), 1.)
        self.assertEqual(task3['ord'], 0.1)
        self.assertEqual(round(task3['urgency'], 3), 1.1)

    def test_plan_can_move_task_down_with_enough_space(self):
        self.report.get_affected_tasks('backlog')
        self.report.move_task_down(1)
        task = self.report.backend.tasks.get(id=1)
        self.assertEqual(task['ord'], 1.5)
        self.assertEqual(round(task['urgency'], 3), 2.5)

    def test_plan_can_move_task_down_without_two_tasks_below_it_half_step(self):
        self.report.get_affected_tasks('doing')
        self.report.move_task_down(7)
        task = self.report.backend.tasks.get(id=7)
        self.assertEqual(task['ord'], -0.75)
        self.assertEqual(round(task['urgency'], 3), 0.25)

    def test_plan_move_down_does_nothing_if_on_bottom(self):
        self.report.get_affected_tasks()
        self.report.move_task_down(6)
        task = self.report.backend.tasks.get(id=6)
        self.assertEqual(task['ord'], None)
        self.assertEqual(round(task['urgency'], 3), 1)

    def test_plan_move_down_pads_tasks_below_if_there_is_no_space(self):
        self.report.move_task_down(4)
        task1 = self.report.backend.tasks.get(id=4)
        task2 = self.report.backend.tasks.get(id=5)
        task3 = self.report.backend.tasks.get(id=6)
        self.assertEqual(task1['ord'], -0.1)
        self.assertEqual(round(task1['urgency'], 3), 0.9)
        self.assertEqual(task2['ord'], None)
        self.assertEqual(round(task2['urgency'], 3), 1.)
        self.assertEqual(task3['ord'], -0.2)
        self.assertEqual(round(task3['urgency'], 3), 0.8)


if __name__ == '__main__':
    unittest.main()
