import pytest
import unittest
from unittest.mock import patch

from taskban import main


class TestMain(unittest.TestCase):

    @patch('taskban.load_parser')
    def test_main_loads_parser(self, parserMock):
        parserMock.parse_args = True
        main()
        self.assertTrue(parserMock.called)

    @patch('taskban.load_parser')
    @patch('taskban.load_logger')
    def test_main_loads_logger(self, loggerMock, parserMock):
        parserMock.parse_args = True
        main()
        self.assertTrue(loggerMock.called)

    @patch('taskban.load_parser')
    @patch('taskban.KanbanReport', autospect=True)
    def test_sync_subcommand(self, taskbanMock, parserMock):
        parserMock.return_value.parse_args.return_value.subcommand = "ocupation"
        main()
        self.assertTrue(
            taskbanMock.called
        )
        self.assertTrue(
            taskbanMock.return_value.print_report.called
        )
