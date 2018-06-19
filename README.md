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

### Ocupation reports

This reports will give the status of the Kanban/scrum board for a specified period of
time with the total time spent in each task:

If not specified the `period` flag it will take the last day modified tasks.

```bash
taskban ocupation
```

The `period` flag must be a taskwarrior time compatible string, for example if
we want to see the information of the tasks modified last week we could use

```bash
taskban ocupation -p 7d
```

Or

```bash
taskban ocupation -p 1w
```

You can also use fixed dates

```bash
taskban ocupation -p 1984-01-01
```

If you want to also show the backlog use the `-b` flag

If you want to also show the tasks that have changed but have an active time of
0 use the `-i` flag.

This report will give you the next information
* *ID*: Task id, if it's completed it will show 0
* *Est*: The number of hours estimated to complete the task
* *Active*: The active time of the task in the specified period
* *Progress*: The percent of progress, between the total time spent in the task
  and the estimate
* *Description*: Description of the task

## Refinement reports

With this mode we'll checkout the backlog, order it and refine it for the next
sprint.

Taskban will be save the status of the refinement in a file in the share
directory. So you can continue the refinement whenever you like.

`taskban refine` will start the refinement process, and it will give you a `task
pro:{{ item }} list` for the first project, If you execute again `taskban refine` it
will give you the same `taskban pro:{{ item }} list`.

With the `next` and `prev` methods you'll navigate through the projects. Keep in
mind that `my-project` is the parent of `my-project.my-subproject` and
`my-subproject` is the child of `my-project`. Also `my-project` and
`my-other-project` are siblings.

With those ideas in mind you can use the following commands:

* `taskban refine next parent`: will jump to the next parent
* `taskban refine next child`: will jump to the next child
* `taskban refine next sibling`: will jump to the next sibling
* `taskban refine prev parent`: will jump to the previous parent
* `taskban refine prev child`: will jump to the previous child
* `taskban refine prev sibling`: will jump to the previous sibling

If you execute `taskban refine next` it will try to jump to the next child, if
it doesn't exist it will try to jump to the next sibling, if it doesn't exist it
will go to the next parent. Same happens in reverse if you use `taskban refine
prev`.

Last but not least, if you want to jump to a specific project execute `taskban
refine jump {{ project }}`

## Planning reports

In the last sprint planning I saw that the task ordering through the ov and pri of
project, subproject and task is not enough, sometimes you need to modify the
order of some tasks without affecting the rest of them.

We needed a tool to order the items in the backlog.

You can use `taskban plan {{ task_id }} up` or `taskban plan {{ task_id }} down`
to move the tasks inside their `pm` status.

Be careful to keep an eye on the ord values of the tasks because it might be
used against the ov and pri values and end up doing things not so important.

You can move tasks only on a project with the `--project {{ project}}` flag, or
you can specify the task status with `--task_status {{ task_status }}`, that
needs to match the `pm` Taskwarrior UDA.

If the desired `ord` doesn't exist in the config, it will create it.
