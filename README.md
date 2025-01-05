# Tasker: simple CLI App

<a href="https://roadmap.sh/projects/task-tracker" target="_blank"></a>
## Description:
Task tracker is a project used to track and manage your tasks.
## Features
The application should run from the command line, accept user actions and inputs as arguments, and store the tasks in a JSON file. The user should be able to:

Add, Update, and Delete tasks
Mark a task as in progress or done
List all tasks
List all tasks that are done
List all tasks that are not done
List all tasks that are in progress
usage: Tasker [-h] {view,add,delete,update,mark_done,mark_in_progress,list} ...

positional arguments:  {view,add,delete,update,mark_done,mark_in_progress,list}
  
    view                Command to view all tasks
    add                 Command to add a task
    delete              Command to delete a task
    update              Command to update a task
    mark_done           Command to mark a task as done
    mark_in_progress    Command to mark a task as in progress
    list                Command to list tasks based on status

options:
  -h, --help            show this help message and exit
