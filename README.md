# Taskban

The program will be used for:
* Sprint planning
* Task mangling
* Retro reports

In combination with [Taskwarrior](taskwarrior.org).

It won't try to replace the Taskwarrior

## Workflow

### Backlog

### Todo

### Doing

### Blocked

### Test

### Done

## Sprint planning

## Task mangling

### Add task to backlog

### Block a task

#### With a reason
#### With a task id

###

## Retro reports

### Kanban reports
This reports will give the status of the kanban board for a specified period of
time with the time spent in each task:

* With a specified period of time we'll print a section for each workflow state
  of the tasks.
* The user must give the period in a taskwarrior date format
* For each section we'll print a list of tasks in that state with the amount of
  time spent in that time for the specified period.
* For the uncompleted tasks, we'll print a ratio of allocated time and total
  spent time on the task.

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
