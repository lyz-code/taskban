import os
import tasklib
import datetime
from tabulate import tabulate


class Report():
    """Abstract class to write reports"""

    def __init__(self, start_date, data_location='~/.task'):
        self.backend = tasklib.TaskWarrior(
            data_location=os.path.expanduser(data_location))
        self.start = start_date
        self._end = self.backend.convert_datetime_string('now')
        self.backend._get_history()
        self.title = ''
        self.content = {}

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
        self.states_order = ['done', 'test', 'blocked', 'doing', 'todo',
                             'backlog']
        self.title = 'Kanban evolution at {}'.format(
            datetime.datetime.now().isoformat())
        self.max_tasks_per_state = 10
        self.create_snapshot()

    def _get_tasks_of_state(self, state):
        '''Get a list of tasks that are in the selected state '''
        if state != 'done':
            return self.backend.tasks.filter(
                status='pending', pm=state, modified__after=self.start)
        else:
            return self.backend.tasks.filter(
                status='completed', modified__after=self.start)

    def create_snapshot(self):
        '''Create a snapshot of the current kanban board, save it on
        self.snapshot in a dictionary where the keys are the states, and in
        each state the keys are the projects'''

        # Extract the tasks
        self.snapshot = {}
        for state in self.available_states.keys():
            for task in self._get_tasks_of_state(state):
                try:
                    self.snapshot[state]
                except KeyError:
                    self.snapshot[state] = {}
                try:
                    self.snapshot[state][task['project']]
                except KeyError:
                    self.snapshot[state][task['project']] = []
                try:
                    task['active_percent'] = \
                        round(100*task.active_time()/(task['est']*3600), 1)
                except TypeError:
                    task['active_percent'] = ' '
                self.snapshot[state][task['project']].append(task)

        # Order the tasks
        for state in self.snapshot.keys():
            for project in self.snapshot[state].keys():
                self.snapshot[state][project] = sorted(
                    self.snapshot[state][project], key=lambda k: k['urgency'])

    def print_report(self, show_backlog=True):
        '''Print the report'''
        print('# {}'.format(self.title))

        for state in self.states_order:
            if state not in self.snapshot.keys() or \
               (state == 'backlog' and show_backlog is False):
                continue
            print('\n## {}'.format(state))
            for project in self.snapshot[state].keys():
                print('\n### {}'.format(project))
                dataset = []
                for task in self.snapshot[state][project]:
                    dataset.append([task['id'],
                                    task['est'],
                                    task['active_percent'],
                                    task['description']])
                    if len(dataset) == self.max_tasks_per_state:
                        break
                print(tabulate(dataset,
                               headers=['ID', 'Est', 'Progress %', 'Description']))
