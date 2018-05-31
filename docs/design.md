In this document we'll write the design docs for the different features

# Sprint review

## Objectives reports

We'll create a report that will take a yaml of objectives and return a score of
completion of the objectives.

The yaml of objectives will have the following structure:

```yaml
name: Objective 1
  ov:
  pri:
  pro:
  subobjectives:
    - name: Subobjective 1
      ov:
      pri:
      pro:
      behaviors:
        - name: Behavior 1
          ov:
          pri:
          accomplished:
        - name: Behavior 2
          ov:
          pri:
          accomplished:
    - name: Subobjective 2
      ...
name: Objective 2
  ...
```

Being `ov` the objective value and `pri` the priority, both numbers between
0 and 5. `pro` will be the associated taskwarrior project. `accomplished` will
be a boolean to fill up each sprint review.

In each sprint review, we'll copy the base template of the objectives and fill
up the accomplished of each one.

This feature will take the weights of objective/subobjective/behaviors from
the taskwarrior config, and calculate the following scores:

* Global score: weighted sum of objectives scores
* Objective scores: weighted sum of the subobjective scores
* Suobjective scores: weighted sum of the behavior scores

It will also be nice to have the variation of the score since the last sprint
review.

### Check objectives/subobjectives priority

We'll have a command `taskban obj obj` that will give a table with the
objectives showing the `ov`, `pri`, `description`, `obj urgency` ordered by `obj
urgency`

We'll have a command `taskban obj subobj` that will give a table with the
subobjectives showing the `ov`, `pri`, `description`, `subobj urgency` ordered
by `subobj urgency`

We'll have a command `taskban obj save` that will update the urgency of the
taskwarrior config file.

### Check the status of the objectives

We will need a cli UI to check the tasks/behaviors of each subobjective and see
a final report of the status of the objectives and it's progression

## Unplanned tasks

Get tasks done added outside the sprint, with total time spent in them vs total time
spent in planned tasks

## Burndown report

Add support for a scrum burndown est report, so we can see the progression of
scope when we add new tasks

## Activity reports

This reports will give the time spent in each task for a selected period of
time.

### Add overall time spent on projects

We'll add support to show the sum of active time in the taskban now report, both
per project and the total

## Progression reports

### Sprint based burndown or history
Get the progression of the project, todo tasks, backlog tasks, overall tasks,
with a prediction of completion, like the burndown.weekly or history but
correctly done by sprint

# Sprint planning

## Objectives sync

Given the objectives yaml template shown [here](#objectives-report), we need
a tool that can specify the weights of the
objective/subobjective/(behaviors|tasks), once we've got them set up maybe in
the taskban config, will calculate the urgency of each taskwarrior project, the
urgency factor of `pri`, `ov` and it will set them on the taskwarrior config.

# Sprint refinement

With this mode we'll checkout the backlog, order it and refine it for the next
sprint.

We'll have a `taskban ref start` and `taskban ref end` to set up the start and
end of an sprint refinement. That will be saved in a file in the share dir of
taskban. So you can continue the refinement whenever you like.

Once the refinement has started:

* If you hit `taskban refine next parent` it will jump to the next parent
* If you hit `taskban refine next child` it will jump to the next child
* If you hit `taskban refine next sibling` it will jump to the next sibling
* If you want to go back `taskban refine prev parent`
* If you want to go back `taskban refine prev child`
* If you want to go back `taskban refine prev sibling`
* If you want to jump to a project `taskban refine jump {{ project }}`
* If you hit `taskban refine next` it will jump to the next child if it exist,
  if not the next sibling if it exist, if not it will go to the next parent
* If you want to go back `taskban refine prev`


* `taskban refine` will give you a `task pro:{{ item }} list` for the first project,
* If you hit again `taskban refine` it will give you the same `taskban pro:{{ item
  }} list`.

`taskban` will save wherever you are in the share file, so you can stop the
refinement whenever you want and continue later

# Task mangling

## Add task to backlog

## Start a task

If there are more than X tasks in doing, force the user to switch some of them
to blocked, todo or even backlog

## Block a task

### With a reason
### With a task id

## Add a task to an active sprint

If I have to add another task outside the sprint planning, make the user select
one of the other tasks so that the amount of estimated time is a constant
inside to
