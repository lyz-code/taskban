import os
import tasklib


class Report():
    def __init__(self, start_date, data_location='~/.task'):
        self.backend = tasklib.TaskWarrior(
            data_location=os.path.expanduser(data_location))
        self.start = start_date
        self.end = '0d'

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = self.backend.convert_datetime_string(
            'now - {}'.format(value))

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self._end = self.backend.convert_datetime_string(
            'now - {}'.format(value))


class KanbanReport(Report):
    pass
