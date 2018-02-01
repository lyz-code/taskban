# import mock
import os
import shutil
import pytest
import tasklib
import unittest
import datetime
import tempfile
from taskban.reports import KanbanReport, Report


class TestReport(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        shutil.rmtree(self.tmp)
        shutil.copytree('test/data', self.tmp)
        self.report = Report(
            data_location=self.tmp,
            taskrc_location=os.path.join(self.tmp, 'taskrc'),
        )

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_set_backend_on_initialize(self):
        self.assertIsInstance(self.report.backend, type(tasklib.TaskWarrior()))

    def test_end_date_of_report_type_datetime(self):
        self.assertIsInstance(self.report._end, type(datetime.datetime.now()))

    def test_end_date_of_report_difference(self):
        self.report = Report(
            '1d',
            data_location=self.tmp,
            taskrc_location=os.path.join(self.tmp, 'taskrc'),
        )
        self.assertEqual(
            self.report._end - self.report.start,
            datetime.timedelta(1),
        )

    def test_set_start_date_of_report_type_datetime(self):
        self.report.start = '1d'
        self.assertIsInstance(self.report.start, type(datetime.datetime.now()))

    def test_start_date_of_report_difference(self):
        self.report = Report(
            '1d',
            data_location=self.tmp,
            taskrc_location=os.path.join(self.tmp, 'taskrc'),
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
            data_location=self.tmp,
            taskrc_location=os.path.join(self.tmp, 'taskrc'),
        )

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_report_has_kanban_states(self):
        self.assertIsInstance(self.report.available_states, dict)

    def test_report_has_kanban_states_order(self):
        self.assertIsInstance(self.report.states_order, list)

    def test_all_available_tests_are_ordered(self):
        self.assertEqual(set(self.report.available_states.keys()),
                         set(self.report.states_order))

    # def test_report_has_list_of_tasks_by_state(self):
    #     for state in self.report.snapshot.keys():
    #         for project in self.report.snapshot[state].keys():
    #             self.assertEqual(
    #                 str(getattr(
    #                 self.report.snapshot[state], project).__class__),
    #                 "<class 'tasklib.task.TaskQuerySet'>")


if __name__ == '__main__':
    unittest.main()
