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
        config_path=None,
        data_path=None,
    ):
        self.config = self.load_yaml(config_path)
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

    def load_yaml(self, yaml_path, no_fail=False):
        try:
            with open(os.path.expanduser(yaml_path), 'r') as f:
                try:
                    return yaml.safe_load(f)
                except yaml.YAMLError as e:
                    log.error(e)
                    raise
        except FileNotFoundError as e:
            if not no_fail:
                log.error('Error opening yaml file {}'.format(yaml_path))
            raise

    def save_yaml(self, yaml_path, dictionary):
        with open(yaml_path, 'w+') as f:
            yaml.dump(dictionary, f, default_flow_style=False)

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
        return self._start

    @start.setter
    def start(self, value):
        """Set up the start of the period to analyze. It must be:
        * a Taskwarrior compatible string to fit in "now - {}".format(value)
        * A date of YYYY-MM-DD.
        * now

        The property will transform it in a datetime object"""
        if re.match('[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}', value):
            datetime_string = value
        elif re.match('now', value):
            datetime_string = 'now'
        else:
            datetime_string = 'now - {}'.format(value)

        self._start_tw_string = datetime_string
        self._start = self.backend.convert_datetime_string(datetime_string)

    def seconds_to_readable(self, seconds):
        second = seconds % 60
        minute = (seconds // 60) % 60
        hour = (seconds // 3600) % 24
        days = (seconds // 86400)

        if days == 0:
            return "{}:{}:{}".format(
                self._number_to_2_digits(hour),
                self._number_to_2_digits(minute),
                self._number_to_2_digits(second),
            )
        else:
            return "{}:{}:{}:{}".format(
                self._number_to_2_digits(days),
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
        data_path=None,
    ):

        super(KanbanReport, self).__init__(
            start_date,
            task_data_path,
            taskrc_path,
            config_path,
            data_path,
        )

        self.title = 'Kanban evolution since {}'.format(self.start.isoformat())
        self.save()

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

    def save(self):
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
                except ZeroDivisionError:
                    task['total_active_percent'] = 'NoEstimate'
                task['active_time'] = \
                    round(task.active_time(self._start_tw_string))
                self.snapshot[state][task['project']].append(task)

        # Order the tasks
        for state in self.snapshot.keys():
            for project in self.snapshot[state].keys():
                self.snapshot[state][project] = sorted(
                    self.snapshot[state][project], key=lambda k: k['urgency'])

    def print_report(
        self,
        show_backlog=True,
        show_inactive=False,
        out=sys.stdout
    ):
        '''Print the report'''
        out.write(
            '# {}'
            '\n\nWarning! Displaying Active time for the selected period but'
            '\nthe Progress is of all the time, so they might mismatch'.format(
                self.title,
            ),
        )

        for state in self.config['states_order']:
            if state not in self.snapshot.keys() or \
               (state == 'backlog' and show_backlog is False):
                continue
            out.write('\n\n## {}'.format(state))
            for project in sorted(self.snapshot[state].keys()):
                dataset = []
                total_active_time = 0
                for task in self.snapshot[state][project]:
                    if task['active_time'] > 0 or show_inactive:
                        dataset.append([task['id'],
                                        task['ov'],
                                        task['est'],
                                        self.seconds_to_readable(
                                            task['active_time']),
                                        task['total_active_percent'],
                                        task['description']])
                        total_active_time += task['active_time']
                    if len(dataset) == self.config['max_tasks_per_state']:
                        break
                total_ov = sum([i[1] for i in dataset if i[1] is not None])
                total_est = sum([i[2] for i in dataset if i[2] is not None])
                from operator import itemgetter
                sorted_dataset = sorted(dataset, key=itemgetter(5))
                sorted_dataset.append([
                    '-----',
                    '---',
                    '---',
                    '--------',
                    '----',
                    '----',
                ])
                sorted_dataset.append([
                    'Total',
                    total_ov,
                    total_est,
                    self.seconds_to_readable(total_active_time),
                    '',
                    '',
                ])
                if len(dataset) > 0:
                    out.write('\n\n### {}\n\n'.format(project))
                    out.write(
                        tabulate(
                            sorted_dataset,
                            headers=[
                                'ID',
                                'OV',
                                'Est',
                                'Active',
                                'Progress %',
                                'Description'
                            ]
                        )
                    )
        out.write('\n')


class RefinementReport(Report):
    """Refinement report, it represents the status of the backlog at the moment

    It will let you jump from project to project to do the refinement"""

    def __init__(
        self,
        start_date='now',
        task_data_path=None,
        taskrc_path=None,
        config_path=None,
        data_path=None,
    ):

        super(RefinementReport, self).__init__(
            start_date,
            task_data_path,
            taskrc_path,
            config_path,
            data_path,
        )
        self.state_file = os.path.join(
            os.path.expanduser(data_path),
            'refinement.yaml',
        )
        self.backend.get_projects()
        self.load()

    def print_report(self):
        'Print the report'
        os.system(
            'TASKDATA={} task rc:{} project:{} list'.format(
                self.config['task_data_path'],
                self.config['taskrc_path'],
                self.state['project'],
            ),
        )

    def end(self):
        'End the refinement, deleting the state file'
        os.remove(self.state_file)

    def save(self):
        'Save the state of the report, the start date, and the current project'
        self.save_yaml(self.state_file, self.state)

    def load(self):
        'Load the state of the report'
        try:
            self.state = self.load_yaml(self.state_file, no_fail=True)
        except FileNotFoundError:
            self.state = {
                'start': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M'),
                'project': sorted(self.backend.projects)[0],
            }
            self.save()

    def find_project_position(self, search_key):
        '''Find the position of the project inside the projects. For example in:

        my-first-project
            my-first-subproject
                my-first-subsubproject
            my-second-subproject
        my-second-project

        self.find_project_position(my-first-project) == [0, 0, 0]
        self.find_project_position(my-second-project) == [1, 0, 0]
        self.find_project_position(
            my-first-project.my-first-subproject,
        ) == [0, 1, 0]
        self.find_project_position(
            my-first-project.my-first-subproject.my-first-subsubproject,
        ) == [0, 0, 1]

        If it doesn't exist it will raise an error
        '''

        for key, value in self.backend.projects.items():
            key_position = sorted(self.backend.projects).index(key)
            if key == search_key:
                return [key_position, 0, 0]
            elif value != {}:
                for subkey, subvalue in value.items():
                    subkey_position = sorted(value).index(subkey)
                    if '{}.{}'.format(key, subkey) == search_key:
                        return [key_position, subkey_position + 1, 0]
                    elif subvalue != {}:
                        for subsubkey, subsubvalue in subvalue.items():
                            subsubkey_position = sorted(subvalue).index(
                                subsubkey,
                            )
                            if '{}.{}.{}'.format(
                                key,
                                subkey,
                                subsubkey,
                            ) == search_key:
                                return [
                                    key_position,
                                    subkey_position + 1,
                                    subsubkey_position + 1,
                                ]
        raise KeyError

    def find_project(self, key_position):
        key = sorted(self.backend.projects)[key_position[0]]
        if key_position[1] == 0:
            return key
        else:
            subkey = sorted(self.backend.projects[key])[key_position[1] - 1]
            if key_position[2] == 0:
                return '{}.{}'.format(key, subkey)
            else:
                subsubkey = sorted(self.backend.projects[key][subkey])[
                    key_position[2] - 1
                ]
                return '{}.{}.{}'.format(key, subkey, subsubkey)

    def _next_child(self, parentage, direction):
        '''Set the next child'''
        if self.project_position[1] == 0:
            self.project_position[1] += direction
            if direction == -1:
                self.project_position[0] += direction
        elif self.project_position[2] == 0:
            self.project_position[2] += direction
            if direction == -1:
                self.project_position[1] += direction
        else:
            raise IndexError

    def _next_sibling(self, parentage, direction):
        '''Set the next sibling'''
        if self.project_position[1] == 0:
            self.project_position[0] += direction
        else:
            if self.project_position[2] == 0:
                self.project_position[1] += direction
            else:
                self.project_position[2] += direction

    def _next_parent(self, parentage, direction):
        '''Set the next sibling'''
        if self.project_position[1] == 0:
            raise IndexError
        elif self.project_position[2] == 0:
            if direction == 1:
                self.project_position[0] += direction
            self.project_position[1] = 0
        else:
            if direction == 1:
                self.project_position[1] += direction
            self.project_position[2] = 0

    def next(self, parentage, direction=1):
        '''Set the next project in the state

        Variable types and examples:

        - parentage:
            - type: String
            - choices: parent, sibling, child
        '''

        self.project_position = self.find_project_position(
            self.state['project'],
        )
        if parentage == 'sibling':
            self._next_sibling(parentage, direction)
        elif parentage == 'child':
            self._next_child(parentage, direction)
        elif parentage == 'parent':
            self._next_parent(parentage, direction)

        self.state['project'] = self.find_project(self.project_position)
        self.save()

    def jump(self, project_name):
        '''Set the current project to project_name'''
        try:
            self.find_project_position(project_name)
            self.state['project'] = project_name
            self.save()
        except KeyError:
            raise


class PlanningReport(Report):
    """Planning report, it will help in the planning of the sprint """

    def __init__(
        self,
        start_date='now',
        task_data_path=None,
        taskrc_path=None,
        config_path=None,
        data_path=None,
        task_state='todo',
        project=None,
    ):

        super(PlanningReport, self).__init__(
            start_date,
            task_data_path,
            taskrc_path,
            config_path,
            data_path,
        )
        self.backend = tasklib.TaskWarrior(
            data_location=os.path.expanduser(task_data_path),
            taskrc_location=os.path.expanduser(taskrc_path),
        )
        self.get_affected_tasks(task_state, project)

    def get_affected_tasks(self, task_state='todo', project=None):
        '''Get all tasks filtered by task_state and possibly by project'''
        if project is None:
            self.tasks = self.backend.tasks.filter(
                pm=task_state,
                status='pending',
            )
        else:
            self.tasks = self.backend.tasks.filter(
                project=project,
                pm=task_state,
                status='pending',
            )
        self.tasks = sorted(
            self.tasks, key=lambda k: k['urgency'],
            reverse=True,
        )

    def _get_task_position(self, task_id):
        'Get task index inside the self.tasks list for a given task_id'
        return [
            index for index, value in enumerate(self.tasks)
            if value['id'] == task_id
        ][0]

    def _increase_task_ord(self, task_id, ord_delta):
        '''Method to increase the ord of a desired task'''
        ord_delta = round(ord_delta, 2)
        task_index = self._get_task_position(task_id)
        if self.tasks[task_index]['ord'] is None:
            self.tasks[task_index]['ord'] = ord_delta
        else:
            self.tasks[task_index]['ord'] += ord_delta
        self.tasks[task_index].save()
        try:
            self.backend.config[
                'urgency.uda.ord.{}.coefficient'.format(
                    self.tasks[task_index]['ord'],
                ),
            ]
        except KeyError:
            self.backend.execute_command([
                'config',
                'urgency.uda.ord.{}.coefficient'.format(
                    self.tasks[task_index]['ord'],
                ),
                self.tasks[task_index]['ord'],
            ])
            self.backend.execute_command([
                'config',
                'urgency.uda.ord.{0:06f}.coefficient'.format(
                    self.tasks[task_index]['ord'],
                ),
                self.tasks[task_index]['ord'],
            ])

    def _move_task(self, task_id, direction):
        task_index = self._get_task_position(task_id)
        if task_index-direction < 0 or \
                task_index-direction > len(self.tasks) - 1:
            # If it's on the extremes return
            return

        urg_delta_to_next_task = (self.tasks[task_index-direction]['urgency'] -
                                  self.tasks[task_index]['urgency'])

        if task_index-2*direction < 0 or \
                task_index-2*direction > len(self.tasks) - 1:
            # If it's one before the last return half the step
            urg_step_above_next_task = urg_delta_to_next_task/2
        else:
            urg_step_above_next_task = (
                self.tasks[task_index-2*direction]['urgency'] -
                self.tasks[task_index-direction]['urgency']
            )/2
            if abs(urg_step_above_next_task) < self.config['minimum_ord_step']:
                self._increase_task_ord(
                    self.tasks[task_index-2*direction]['id'],
                    2 * direction * self.config['minimum_ord_step'],
                )
                urg_step_above_next_task = \
                    self.config['minimum_ord_step'] * direction
        self._increase_task_ord(
            self.tasks[task_index]['id'],
            urg_delta_to_next_task + urg_step_above_next_task,
        )

    def move_task_up(self, task_id):
        self._move_task(task_id, 1)

    def move_task_down(self, task_id):
        self._move_task(task_id, -1)
