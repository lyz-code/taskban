import pytest
import unittest
from unittest.mock import patch, call

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
        parserMock.return_value.parse_args.return_value.subcommand = 'ocupation'
        main()
        self.assertTrue(taskbanMock.called)
        self.assertTrue(
            taskbanMock.return_value.print_report.called,
        )

    @patch('taskban.load_parser')
    @patch('taskban.RefinementReport', autospect=True)
    def test_has_refine_subcommand(self, taskbanMock, parserMock):
        parserMock.return_value.parse_args.return_value.subcommand = 'refine'
        main()
        self.assertTrue(taskbanMock.called)

    @patch('taskban.load_parser')
    @patch('taskban.RefinementReport', autospect=True)
    @patch('taskban.os')
    def test_refine_executes_task_command_by_default(
        self,
        osMock,
        taskbanMock,
        parserMock,
    ):
        parser = parserMock.return_value.parse_args.return_value
        parser.subcommand = 'refine'
        parser.taskrc_path = '~/.task/taskrc'
        taskbanMock.return_value.state = {'project': 'my-first-project'}
        main()
        self.assertEqual(
            osMock.system.assert_called_with(
                'task rc:~/.task/taskrc pro:my-first-project list',
            ),
            None,
        )

    @patch('taskban.load_parser')
    @patch('taskban.RefinementReport', autospect=True)
    def test_refine_jump_to_project(self, taskbanMock, parserMock):
        parser = parserMock.return_value.parse_args.return_value
        parser.subcommand = 'refine'
        parser.next_subcommand = 'jump'
        parser.jump_project = 'my-project'
        main()
        self.assertTrue(taskbanMock.called)
        self.assertEqual(
            taskbanMock.return_value.jump.assert_called_with('my-project'),
            None,
        )

    @patch('taskban.load_parser')
    @patch('taskban.RefinementReport', autospect=True)
    def test_refine_next_parent(self, taskbanMock, parserMock):
        parser = parserMock.return_value.parse_args.return_value
        parser.subcommand = 'refine'
        parser.next_subcommand = 'next'
        parser.parentage = 'parent'
        main()
        self.assertTrue(taskbanMock.called)
        self.assertEqual(
            taskbanMock.return_value.next.assert_called_with('parent', 1),
            None,
        )

    @patch('taskban.load_parser')
    @patch('taskban.RefinementReport', autospect=True)
    def test_refine_next_parent_doesnt_fail_at_end(
        self,
        taskbanMock,
        parserMock,
    ):
        parser = parserMock.return_value.parse_args.return_value
        parser.subcommand = 'refine'
        parser.next_subcommand = 'next'
        parser.parentage = 'parent'
        taskbanMock.return_value.next.side_effect = IndexError
        main()
        self.assertTrue(taskbanMock.called)
        self.assertTrue(taskbanMock.return_value.end.called)
        self.assertEqual(
            taskbanMock.return_value.next.assert_called_with('parent', 1),
            None,
        )

    @patch('taskban.load_parser')
    @patch('taskban.RefinementReport', autospect=True)
    def test_refine_next_child(self, taskbanMock, parserMock):
        parser = parserMock.return_value.parse_args.return_value
        parser.subcommand = 'refine'
        parser.next_subcommand = 'next'
        parser.parentage = 'child'
        main()
        self.assertTrue(taskbanMock.called)
        self.assertEqual(
            taskbanMock.return_value.next.assert_called_with('child', 1),
            None,
        )

    @patch('taskban.load_parser')
    @patch('taskban.RefinementReport', autospect=True)
    def test_refine_next_child_doesnt_fail_at_end(
        self,
        taskbanMock,
        parserMock,
    ):
        parser = parserMock.return_value.parse_args.return_value
        parser.subcommand = 'refine'
        parser.next_subcommand = 'next'
        parser.parentage = 'child'
        taskbanMock.return_value.next.side_effect = IndexError
        main()
        self.assertTrue(taskbanMock.called)
        self.assertEqual(
            taskbanMock.return_value.next.assert_called_with('child', 1),
            None,
        )

    @patch('taskban.load_parser')
    @patch('taskban.RefinementReport', autospect=True)
    def test_refine_next_sibling(self, taskbanMock, parserMock):
        parser = parserMock.return_value.parse_args.return_value
        parser.subcommand = 'refine'
        parser.next_subcommand = 'next'
        parser.parentage = 'sibling'
        main()
        self.assertTrue(taskbanMock.called)
        self.assertEqual(
            taskbanMock.return_value.next.assert_called_with('sibling', 1),
            None,
        )

    @patch('taskban.load_parser')
    @patch('taskban.RefinementReport', autospect=True)
    def test_refine_next_sibling_doesnt_fail_at_end(
        self,
        taskbanMock,
        parserMock,
    ):
        parser = parserMock.return_value.parse_args.return_value
        parser.subcommand = 'refine'
        parser.next_subcommand = 'next'
        parser.parentage = 'sibling'
        taskbanMock.return_value.next.side_effect = IndexError
        main()
        self.assertTrue(taskbanMock.called)
        self.assertEqual(
            taskbanMock.return_value.next.assert_called_with('sibling', 1),
            None,
        )

    @patch('taskban.load_parser')
    @patch('taskban.RefinementReport', autospect=True)
    def test_refine_next_to_child_if_it_exists(self, taskbanMock, parserMock):
        parser = parserMock.return_value.parse_args.return_value
        parser.subcommand = 'refine'
        parser.next_subcommand = 'next'
        main()
        self.assertTrue(taskbanMock.called)
        self.assertEqual(
            taskbanMock.return_value.next.assert_called_with('child', 1),
            None,
        )

    @patch('taskban.load_parser')
    @patch('taskban.RefinementReport', autospect=True)
    def test_refine_next_to_sibling_if_child_doesnt_exists(
        self,
        taskbanMock,
        parserMock,
    ):
        parser = parserMock.return_value.parse_args.return_value
        parser.subcommand = 'refine'
        parser.next_subcommand = 'next'

        def child_doesnt_exist(parentage, *args, **kwargs):
            if parentage == 'child':
                raise IndexError
            else:
                pass

        taskbanMock.return_value.next.side_effect = child_doesnt_exist
        main()
        self.assertTrue(taskbanMock.called)
        self.assertEqual(
            taskbanMock.return_value.next.mock_calls,
            [call('child', 1), call('sibling', 1)],
        )

    @patch('taskban.load_parser')
    @patch('taskban.RefinementReport', autospect=True)
    def test_refine_next_to_parent_if_child_and_sibling_dont_exists(
        self,
        taskbanMock,
        parserMock,
    ):
        parser = parserMock.return_value.parse_args.return_value
        parser.subcommand = 'refine'
        parser.next_subcommand = 'next'

        def child_doesnt_exist(parentage, *args, **kwargs):
            if parentage == 'child' or parentage == 'sibling':
                raise IndexError
            else:
                pass

        taskbanMock.return_value.next.side_effect = child_doesnt_exist
        main()
        self.assertTrue(taskbanMock.called)
        self.assertEqual(
            taskbanMock.return_value.next.mock_calls,
            [call('child', 1), call('sibling', 1), call('parent', 1)],
        )

    @patch('taskban.load_parser')
    @patch('taskban.RefinementReport', autospect=True)
    def test_refine_next_dont_error_if_parent_dont_exists(
        self,
        taskbanMock,
        parserMock,
    ):
        parser = parserMock.return_value.parse_args.return_value
        parser.subcommand = 'refine'
        parser.next_subcommand = 'next'

        taskbanMock.return_value.next.side_effect = IndexError
        main()
        self.assertTrue(taskbanMock.called)
        self.assertEqual(
            taskbanMock.return_value.next.mock_calls,
            [call('child', 1), call('sibling', 1), call('parent', 1)],
        )
        self.assertTrue(taskbanMock.return_value.end.called)

    @patch('taskban.load_parser')
    @patch('taskban.RefinementReport', autospect=True)
    def test_refine_prev_parent(self, taskbanMock, parserMock):
        parser = parserMock.return_value.parse_args.return_value
        parser.subcommand = 'refine'
        parser.next_subcommand = 'prev'
        parser.parentage = 'parent'
        main()
        self.assertTrue(taskbanMock.called)
        self.assertEqual(
            taskbanMock.return_value.next.assert_called_with('parent', -1),
            None,
        )

    @patch('taskban.load_parser')
    @patch('taskban.RefinementReport', autospect=True)
    def test_refine_prev_parent_doesnt_fail_at_beggining(
        self,
        taskbanMock,
        parserMock,
    ):
        parser = parserMock.return_value.parse_args.return_value
        parser.subcommand = 'refine'
        parser.next_subcommand = 'prev'
        parser.parentage = 'parent'
        taskbanMock.return_value.next.side_effect = IndexError
        main()
        self.assertTrue(taskbanMock.called)
        self.assertFalse(taskbanMock.return_value.end.called)
        self.assertEqual(
            taskbanMock.return_value.next.assert_called_with('parent', -1),
            None,
        )

    @patch('taskban.load_parser')
    @patch('taskban.RefinementReport', autospect=True)
    def test_refine_prev_child(self, taskbanMock, parserMock):
        parser = parserMock.return_value.parse_args.return_value
        parser.subcommand = 'refine'
        parser.next_subcommand = 'prev'
        parser.parentage = 'child'
        main()
        self.assertTrue(taskbanMock.called)
        self.assertEqual(
            taskbanMock.return_value.next.assert_called_with('child', -1),
            None,
        )

    @patch('taskban.load_parser')
    @patch('taskban.RefinementReport', autospect=True)
    def test_refine_prev_child_doesnt_fail_at_end(
        self,
        taskbanMock,
        parserMock,
    ):
        parser = parserMock.return_value.parse_args.return_value
        parser.subcommand = 'refine'
        parser.next_subcommand = 'prev'
        parser.parentage = 'child'
        taskbanMock.return_value.next.side_effect = IndexError
        main()
        self.assertTrue(taskbanMock.called)
        self.assertEqual(
            taskbanMock.return_value.next.assert_called_with('child', -1),
            None,
        )

    @patch('taskban.load_parser')
    @patch('taskban.RefinementReport', autospect=True)
    def test_refine_prev_sibling(self, taskbanMock, parserMock):
        parser = parserMock.return_value.parse_args.return_value
        parser.subcommand = 'refine'
        parser.next_subcommand = 'prev'
        parser.parentage = 'sibling'
        main()
        self.assertTrue(taskbanMock.called)
        self.assertEqual(
            taskbanMock.return_value.next.assert_called_with('sibling', -1),
            None,
        )

    @patch('taskban.load_parser')
    @patch('taskban.RefinementReport', autospect=True)
    def test_refine_prev_sibling_doesnt_fail_at_end(
        self,
        taskbanMock,
        parserMock,
    ):
        parser = parserMock.return_value.parse_args.return_value
        parser.subcommand = 'refine'
        parser.next_subcommand = 'prev'
        parser.parentage = 'sibling'
        taskbanMock.return_value.next.side_effect = IndexError
        main()
        self.assertTrue(taskbanMock.called)
        self.assertEqual(
            taskbanMock.return_value.next.assert_called_with('sibling', -1),
            None,
        )

    @patch('taskban.load_parser')
    @patch('taskban.RefinementReport', autospect=True)
    def test_refine_prev_to_child_if_it_exists(self, taskbanMock, parserMock):
        parser = parserMock.return_value.parse_args.return_value
        parser.subcommand = 'refine'
        parser.next_subcommand = 'prev'
        main()
        self.assertTrue(taskbanMock.called)
        self.assertEqual(
            taskbanMock.return_value.next.assert_called_with('child', -1),
            None,
        )

    @patch('taskban.load_parser')
    @patch('taskban.RefinementReport', autospect=True)
    def test_refine_prev_to_sibling_if_child_doesnt_exists(
        self,
        taskbanMock,
        parserMock,
    ):
        parser = parserMock.return_value.parse_args.return_value
        parser.subcommand = 'refine'
        parser.next_subcommand = 'prev'

        def child_doesnt_exist(parentage, *args, **kwargs):
            if parentage == 'child':
                raise IndexError
            else:
                pass

        taskbanMock.return_value.next.side_effect = child_doesnt_exist
        main()
        self.assertTrue(taskbanMock.called)
        self.assertEqual(
            taskbanMock.return_value.next.mock_calls,
            [call('child', -1), call('sibling', -1)],
        )

    @patch('taskban.load_parser')
    @patch('taskban.RefinementReport', autospect=True)
    def test_refine_prev_to_parent_if_child_and_sibling_dont_exists(
        self,
        taskbanMock,
        parserMock,
    ):
        parser = parserMock.return_value.parse_args.return_value
        parser.subcommand = 'refine'
        parser.next_subcommand = 'prev'

        def child_doesnt_exist(parentage, *args, **kwargs):
            if parentage == 'child' or parentage == 'sibling':
                raise IndexError
            else:
                pass

        taskbanMock.return_value.next.side_effect = child_doesnt_exist
        main()
        self.assertTrue(taskbanMock.called)
        self.assertEqual(
            taskbanMock.return_value.next.mock_calls,
            [call('child', -1), call('sibling', -1), call('parent', -1)],
        )

    @patch('taskban.load_parser')
    @patch('taskban.RefinementReport', autospect=True)
    def test_refine_prev_dont_error_if_parent_dont_exists(
        self,
        taskbanMock,
        parserMock,
    ):
        parser = parserMock.return_value.parse_args.return_value
        parser.subcommand = 'refine'
        parser.next_subcommand = 'prev'

        taskbanMock.return_value.next.side_effect = IndexError
        main()
        self.assertTrue(taskbanMock.called)
        self.assertEqual(
            taskbanMock.return_value.next.mock_calls,
            [call('child', -1), call('sibling', -1), call('parent', -1)],
        )
        self.assertFalse(taskbanMock.return_value.end.called)
