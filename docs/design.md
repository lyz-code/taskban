In this document we'll write the design docs for the different features

# Sprint review

## Objectives report

We'll have a new uda `it` called `Item Type` which will be one of:
* history
* epic
* behavior
* project

The `history` type is the common tasks. `epic` are the tasks that have a meaning
towards a life objective, those are the ones defined in the objectives.md file
under project.management. `behaviors` are behaviors that I want to implement or
I'm implementing. And `project` will be a type of issue managed by taskban to
set up the priority and ov of the different projects and subprojects.

I've set reports for each of this types so it's cleaner to see them when you
want to

### Projects

If you change the ov or priority of the projects, taskban will recalculate the
urgency score and set it up on your config file.

As both history and epics share the project you'll priorize both at the same
time.

They'll have an uda called `td` (`task_description`) where we'll store the
information of the task

### Behaviors

At the end of the sprint we'll execute a behavior report, in which the user will
answer yes or no if they have accomplished the desired behavior (only the ones
with `pm:todo`), if you have accomplished it, it will reduce it's priority by
X points and if you haven't it will increase it's importance.

In each sprint you should focus on the Y first behaviors.

### Epics

Epics are a way of organize what you want to do in each project. It's meant to
be breaking points in them.

Once you've got all set up, you should priorize them, and adjust the project ov
and pri so they match your desired order.

## Deprecated Objectives reports

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

## Sprint goal checker

With this tool you'll set up the maximum value of an uda (such as `est`) and it
will check if your `todo` + `doing` + `blocked` tasks add up that score.

* It should also be a good idea to select the % of points spent in each project.
  of the % of each project you should be able to specify the % of the
  subprojects, and so on.

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
