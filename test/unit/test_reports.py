# import mock
import tasklib
import unittest
import datetime
from taskban.reports import KanbanReport, Report


class TestReport(unittest.TestCase):
    def setUp(self):
        self.report = Report('1d')

    def test_report_object_can_be_created(self):
        self.assertIsInstance(self.report, type(Report('1d')))

    def test_set_backend_on_initialize(self):
        self.assertIsInstance(self.report.backend, type(tasklib.TaskWarrior()))

    def test_end_date_of_report_type_datetime(self):
        self.assertIsInstance(self.report._end, type(datetime.datetime.now()))

    def test_end_date_of_report_difference(self):
        self.assertEqual(self.report._end - self.report.start,
                         datetime.timedelta(1))

    def test_set_start_date_of_report_type_datetime(self):
        self.report.start = '1d'
        self.assertIsInstance(self.report.start, type(datetime.datetime.now()))

    def test_start_date_of_report_difference(self):
        self.assertEqual(self.report._end - self.report.start,
                         datetime.timedelta(1))

    def test_report_has_history(self):
        self.assertIsInstance(self.report.backend.history, list)

    def test_report_report_has_title(self):
        self.assertIsInstance(self.report.title, str)

    def test_report_report_has_content(self):
        self.assertIsInstance(self.report.content, dict)


class TestKanbanReport(unittest.TestCase):
    def setUp(self):
        self.report = KanbanReport('1d')

    def test_kanban_report_object_can_be_created(self):
        self.assertIsInstance(self.report, type(KanbanReport('1d')))

    def test_report_has_kanban_states(self):
        self.assertIsInstance(self.report.available_states, dict)

    def test_report_has_kanban_states_order(self):
        self.assertIsInstance(self.report.states_order, set)

    def test_all_available_tests_are_ordered(self):
        self.assertEqual(set(self.report.available_states.keys()),
                         self.report.states_order)

    def test_report_has_list_of_tasks_by_state(self):
        for state in self.report.available_states.keys():
            self.assertEqual(str(getattr(self.report, state).__class__),
                             "<class 'tasklib.task.TaskQuerySet'>")

if __name__ == '__main__':
    unittest.main()
