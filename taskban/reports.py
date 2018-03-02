import os
import re
import sys
import yaml
import tasklib
import logging
import datetime
from tabulate import tabulate

log = logging.getLogger('Main')


class Report():
    """Abstract class to write reports"""

    def __init__(
        self,
        start_date=None,
        task_data_path=None,
        taskrc_path=None,
        config_path='~/.local/share/taskban/config.yaml',
    ):
        self.load_config(config_path)
        self.update_config_with_arguments(
            start_date,
            task_data_path,
            taskrc_path,
            config_path,
        )
        self.backend = tasklib.TaskWarrior(
            data_location=os.path.expanduser(task_data_path),
            taskrc_location=os.path.expanduser(taskrc_path),
        )
        self.start = self.config['start_date']
        self.backend.history.get_history()
        self._end = self.backend.convert_datetime_string('now')
        self.title = ''
        self.content = {}

    def load_config(self, config_path):
        try:

            with open(os.path.expanduser(config_path), 'r') as f:
                try:
                    self.config = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    log.error(e)
                    raise
        except FileNotFoundError as e:
            log.error('Error opening config file {}'.format(config_path))
            raise

    def update_config_with_arguments(
        self,
        start_date,
        task_data_path,
        taskrc_path,
        config_path,
    ):
        arguments = locals()
        for argument, value in arguments.items():
            if value is not None:
                self.config[argument] = value

    @property
    def start(self):
        """Set up the start of the period to analyze. It must be a Taskwarrior
        compatible string to fit in "now - {}".format(value).

        The property will transform it in a datetime object"""
        return self._start

    @start.setter
    def start(self, value):
        if isinstance(value, datetime.date):
            datetime_string = value.strftime('%Y-%m-%dT%H:%M:%S')
        elif re.match('[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}', value):
            datetime_string = value
        else:
            datetime_string = 'now - {}'.format(value)

        self._start_tw_string = datetime_string
        self._start = self.backend.convert_datetime_string(datetime_string)

    def seconds_to_readable(self, seconds):
        second = seconds % 60
        minute = (seconds // 60) % 60
        hour = (seconds // 3600) % 24
        # days = (seconds // 86400)

        return "{}:{}:{}".format(
            self._number_to_2_digits(hour),
            self._number_to_2_digits(minute),
            self._number_to_2_digits(second),
        )

    def _number_to_2_digits(self, n):
        return repr(round(n)).zfill(2)


class KanbanReport(Report):
    """Kanban report, it represents the status of the board at the moment, with
    the time tracking since self.start.

    It is divided into the different states of the tasks, this must match the
    Taskwarrior `pm` UDA.

    Each state is subdivided in projects"""

    def __init__(
        self,
        start_date=None,
        task_data_path=None,
        taskrc_path=None,
        config_path=None,
    ):

        super(KanbanReport, self).__init__(
            start_date,
            task_data_path,
            taskrc_path,
            config_path,
        )

        self.title = 'Kanban evolution since {}'.format(self.start.isoformat())
        self.create_snapshot()

    def _get_tasks_of_state(self, state):
        '''Get a list of tasks that are in the selected state '''
        if state != 'done':
            return self.backend.tasks.filter(
                status='pending',
                pm=state,
                modified__after=self.start,
            )
        else:
            return self.backend.tasks.filter(
                status='completed',
                modified__after=self.start,
            )

    def create_snapshot(self):
        '''Create a snapshot of the current kanban board, save it on
        self.snapshot in a dictionary where the keys are the states, and in
        each state the keys are the projects'''

        # Extract the tasks
        self.snapshot = {}
        for state in self.config['available_states'].keys():
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
                    task['total_active_percent'] = \
                        round(100*task.active_time()/(task['est']*3600), 1)
                except TypeError:
                    task['total_active_percent'] = ''
                task['active_time'] = \
                    round(task.active_time(self._start_tw_string))
                self.snapshot[state][task['project']].append(task)

        # Order the tasks
        for state in self.snapshot.keys():
            for project in self.snapshot[state].keys():
                self.snapshot[state][project] = sorted(
                    self.snapshot[state][project], key=lambda k: k['urgency'])

    def print_report(self, show_backlog=True, out=sys.stdout):
        '''Print the report'''
        out.write('# {}'.format(self.title))

        for state in self.config['states_order']:
            if state not in self.snapshot.keys() or \
               (state == 'backlog' and show_backlog is False):
                continue
            out.write('\n\n## {}'.format(state))
            for project in self.snapshot[state].keys():
                out.write('\n\n### {}\n\n'.format(project))
                dataset = []
                for task in self.snapshot[state][project]:
                    dataset.append([task['id'],
                                    task['est'],
                                    self.seconds_to_readable(
                                        task['active_time']),
                                    task['total_active_percent'],
                                    task['description']])
                    if len(dataset) == self.config['max_tasks_per_state']:
                        break
                out.write(
                    tabulate(
                        dataset,
                        headers=[
                            'ID',
                            'Est',
                            'Active',
                            'Progress %',
                            'Description'
                        ]
                    )
                )
