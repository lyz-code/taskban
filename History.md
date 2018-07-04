
v0.5.3 / 2018-07-04
==================

  * Added tox
  * Added ignore-io python gitignore
  * Fixed the saving of the wrong ord in the taskrc file

v0.5.2 / 2018-06-28
===================

  * Added days to the seconds_to_readable method

v0.5.1 / 2018-06-28
===================

  * Don't add nones in the total sum of est and ov

v0.5.0 / 2018-06-26
===================

  * Fix delay on tw loading because of inheritance * Fix task order sorted by urgency * Round the ord to the second decimal * Fix the saving of the configuration
  * Create plan move argparse
  * Add method move_task_down
  * Allow taskban to edit the configuration adding the ord if it doesn't exist
  * Removed age from the urgency calculation
  * Added pending tasks to complete the feature
  * Added _increase_task_ord method * Upgraded tasklib version to have the save_config method
  * Added _get_task_position method
  * Added get_afected_tasks method
  * Added sprint goal checker design docs
  * Added initial design docs for sprint planning task ordering

v0.4.0 / 2018-06-21
===================

  * Added total values to the ocupation report

v0.3.1 / 2018-06-02
===================

  * Order the output of the ocupation command
  * Upgrade version of package

v0.3.0 / 2018-06-02
===================

  * Completed README
  * Changed the way the projects are saved
  * Add refinement commands
  * Added refinement parsers
  * Change now to ocupation as subcommand
  * Added tests for the logger and init
  * Implemented jump method
  * Implemented previous method
  * Refine the next method
  * Implemented parent method
  * Added find_project_position and find_project methods
  * Refinement report complete print_report method
  * Updated tasklib to v0.2.0 * WIP: list projects
  * Add end method for refinement report
  * Initialize refinement state if empty
  * Add support for absent state file
  * Added support for load in refinement report
  * Added support for save_yaml
  * Refactor load_config to load_yaml
  * Refactored files * Corrected description of arguments * Added now to start project * Added first version of refinement

v0.2.0 / 2018-05-04
===================

  * Removed history.cache from git index
  * modified history.cache
  * Added -i flag for taskban report now

v0.1.3 / 2018-05-04
===================

  * Sprint refinement docs

v0.1.2 / 2018-04-16
===================

  * Stabilize tasklib version * Add NoEstimate label to unestimated tasks
  * Reorder documentation

v0.1.1 / 2018-03-05
===================

  * Upgraded version on setup.py
  * Make subcommand mandatory
  * Completed Readme.md * Added test for tasks with estimate 0

v0.1.0 / 2018-03-02
===================

  * Fix pytest --converge error
  * Fixed version in setup py
  * Display the disclaimer of the active time
  * Reordered Readme * Added parsers for the taskwarrior data location
  * Load config in the report
  * Added tests for the argparse function * Advanced in the test of the printed report
  * Add support for other types of dates more than now - {} * Add more tests
  * refactored TestKanbanReport to the new tasklib
  * Refactor after tasklib test development * Added first version of default test data * Added Install and test to readme.md * Fixed format to complain with the new standards
  * [feat] start a task
  * [wip] add data_location argument
  * [feat] add active time to kanban report
  * [feat] update readme [feat] first version of taskban now report [feat] package the program
  * [feat] argcomplete
  * [gitignore] update
  * [report] add title and content
  * [kanbanreport] get available states
  * license and gitignore
