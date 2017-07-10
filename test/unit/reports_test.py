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

    def test_set_end_date_of_report_type_datetime(self):
        self.report.end = '1d'
        self.assertIsInstance(self.report.end, type(datetime.datetime.now()))

    def test_end_date_of_report_difference(self):
        report1 = Report('1d')
        report1.end = '1d'
        self.assertEqual(self.report.end - report1.end, datetime.timedelta(1))

    def test_set_start_date_of_report_type_datetime(self):
        self.report.start = '1d'
        self.assertIsInstance(self.report.start, type(datetime.datetime.now()))

    def test_start_date_of_report_difference(self):
        self.assertEqual(self.report.end - self.report.start,
                         datetime.timedelta(1))


class TestKanbanReport(unittest.TestCase):
    def test_kanban_report_object_an_be_created(self):
        kanban_report = KanbanReport('1d')
        self.assertIsInstance(kanban_report, type(KanbanReport('1d')))


if __name__ == '__main__':
    unittest.main()
