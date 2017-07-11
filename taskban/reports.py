import os
import tasklib


class Report():
    """Abstract class to write reports"""

    def __init__(self, start_date, data_location='~/.task'):
        self.backend = tasklib.TaskWarrior(
            data_location=os.path.expanduser(data_location))
        self.start = start_date
        self._end = self.backend.convert_datetime_string('now')
        self.backend._get_history()

    @property
    def start(self):
        """Set up the start of the period to analyze. It must be a Taskwarrior
        compatible string to fit in "now - {}".format(value).

        The property will transform it in a datetime object"""
        return self._start

    @start.setter
    def start(self, value):
        self._start = self.backend.convert_datetime_string(
            'now - {}'.format(value))


class KanbanReport(Report):
    """Kanban report, it represents the status of the board at the moment, with
    the time tracking since self.start.

    It is divided into the different states of the tasks, this must match the
    Taskwarrior `pm` UDA.

    Each state is subdivided in projects"""

    def __init__(self, start_date, data_location='~/.task'):
        super(KanbanReport, self).__init__(start_date, data_location)
        self.available_states = {'todo': 'To Do', 'doing': 'Doing',
                                 'done': 'Done', 'blocked': 'Blocked',
                                 'test': 'Testing', 'backlog': 'Backlog'}
        self.states_order = {'done', 'test', 'blocked', 'doing', 'todo',
                             'backlog'}

        for state in self.available_states.keys():
            self.get_tasks_of_state(state)

    def get_tasks_of_state(self, state):
        '''Set a list of tasks that are in the selected state under
        self.state'''

        if state != 'done':
            status = 'pending'
        else:
            status = 'completed'

        setattr(self, state, self.backend.tasks.filter(status=status,
                                                       kanban=state))
