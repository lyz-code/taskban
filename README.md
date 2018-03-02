# Taskban

The program will be used for:
* Sprint planning
* Task mangling
* Retro reports

It works in combination with [Taskwarrior](taskwarrior.org) so it won't try to
replace it.

## Install

Clone the repository and install it

```bash
git clone https://github.com/lyz-code/taskban
cd taskban
pip install -r requirements.txt
python3 setup.py install
```

## Test

```bash
pip install -r requirements-tests.txt
pytest
```

## Retro reports

### Kanban reports

This reports will give the status of the Kanban board for a specified period of
time with the total time spent in each task:

If not specified the `period` flag it will take the last day modified tasks.

```bash
taskban now
```

The `period` flag must be a taskwarrior time compatible string, for example if
we want to see the information of the tasks modified last week we could use

```bash
taskban now -p 7d
```

Or

```bash
taskban now -p 1w
```

You can also use fixed dates

```bash
taskban now -p 1984-01-01
```

If you want to also show the backlog use the `-b` flag

This report will give you the next information
* *ID*: Task id, if it's completed it will show 0
* *Est*: The number of hours estimated to complete the task
* *Active*: The active time of the task in the specified period
* *Progress*: The percent of progress, between the total time spent in the task
  and the estimate
* *Description*: Description of the task

### Activity reports

This reports will give the time spent in each task for a selected period of
time.

* We'll have two specified periods, the period of analysis of tasks, and the
  period of subdivisions. For example, we'd like a report of the last week
  subdivided by days
* We'll print a section on each subdivision with a list of tasks and their
  active time.
* Finally we'll add up all the active time per subdivision and the sum up of all
  the active time of the period

### Estimation reports


## Sprint planning

## Task mangling

### Add task to backlog

### Start a task

If there are more than X tasks in doing, force the user to switch some of them
to blocked, todo or even backlog

### Block a task

#### With a reason
#### With a task id

### Add a task to an active sprint

If I have to add another task outside the sprint planning, make the user select
one of the other tasks so that the amount of estimated time is a constant
inside to
