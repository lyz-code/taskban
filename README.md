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

You should use the following UDAs in your taskwarrior tasks
* `est`: Estimate of the task
* `pm`: The state of the task

My suggestion would be to add this lines to your `taskrc`

```
uda.pm.type=string
uda.pm.label=Kanban
uda.pm.values=todo,doing,done,blocked,test,backlog
uda.pm.default=backlog

uda.est.type=numeric
uda.est.label=Estimate
```

If you have a lot of activity in taskwarrior, the parsing of the history might
be heavy, so I also suggest to use the history parsing cache, so add to your
`taskrc`

```
history.cache=15d
history.cache.location=history.cache
```

## Test

```bash
pip install -r requirements-tests.txt
pytest
```

## Retro reports

### Board reports

This reports will give the status of the Kanban/scrum board for a specified period of
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

