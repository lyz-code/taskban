In this document we'll write the design docs for the different features

# Retro reports

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


## Activity reports

This reports will give the time spent in each task for a selected period of
time.

* We'll have two specified periods, the period of analysis of tasks, and the
  period of subdivisions. For example, we'd like a report of the last week
  subdivided by days
* We'll print a section on each subdivision with a list of tasks and their
  active time.
* Finally we'll add up all the active time per subdivision and the sum up of all
  the active time of the period

## Estimation reports


# Sprint planning

## Objectives sync

Given the objectives yaml template shown [here](#objectives-report), we need
a tool that can specify the weights of the
objective/subobjective/(behaviors|tasks), once we've got them set up maybe in
the taskban config, will calculate the urgency of each taskwarrior project, the
urgency factor of `pri`, `ov` and it will set them on the taskwarrior config.

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
