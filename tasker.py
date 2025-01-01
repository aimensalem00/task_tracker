import argparse
from datetime import datetime
import json
import os
from typing import Literal
from tabulate import tabulate

def create_parser():
    # main parser
    parser = argparse.ArgumentParser(prog='Tasker', description='"Tasker" a simple task manager')
    # subparsers for different commands
    subparsers = parser.add_subparsers(dest='command',help='sub-command help')
    # view all tasks
    view_parser = subparsers.add_parser('view', help='Command to view all tasks')
    view_parser.add_argument('all', type=str, help='Task number to be viewed')
    # Subparser for "add" command
    add_parser = subparsers.add_parser('add', help='Command to add a task')
    add_parser.add_argument('task_description', type=str, help='Task to be added')
    # Subparser for "delete" command
    delete_parser = subparsers.add_parser('delete', help='Command to delete a task')
    delete_parser.add_argument('task_id', type=int, help='Task number to be deleted')
    # Subparser for "update" command
    update_parser = subparsers.add_parser('update', help='Command to update a task')
    update_parser.add_argument('task_id', type=int, help='Task number to be updated')
    update_parser.add_argument('task_description', type=str, help='Task to be updated')
    # Subparser for "mark_done" command
    mark_done_parser = subparsers.add_parser('mark_done', help='Command to mark a task as done')
    mark_done_parser.add_argument('task_id', type=int, help='Task number to be marked as done')
    # Subparser for "mark_in_progress" command
    mark_in_progress_parser = subparsers.add_parser('mark_in_progress', help='Command to mark a task as in progress')
    mark_in_progress_parser.add_argument('task_id', type=int, help='Task number to be marked as in progress')
    # Subparser for "list" command
    list_parser = subparsers.add_parser('list', help='Command to list tasks based on status')
    list_parser.add_argument('status', type=str, choices=['to-do', 'in-progress', 'done'], help='Status of the tasks to be listed')
    return parser

# Check the JSON file
def check_json(file_path):
    if not os.path.exists(file_path):
        return False
    else:
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
                if not data:
                    # The JSON file contains an empty structure (lists only).
                    return True
                else:
                    # The JSON file is not empty.
                    return True
            except json.JSONDecodeError:
                print("The file does not contain valid JSON.")
                return False

# Generate the next numeric ID based on the existing tasks (used when adding new task).
def get_next_id(tasks):
    if not tasks:
        return 1  # Start from 1 if no tasks exist
    return max(task["id"] for task in tasks) + 1

'''Methods to handle the arguments'''
# View all tasks
def view_all_tasks(all, file_path):
    # Load the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)
    if not data:
        print('No tasks found!')
        return
    else:
        # Tabulate table
        print(tabulate(data, headers="keys", tablefmt="fancy_grid"))

# Add a task
def add_task(task, file_path):
    # Load the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)
    # Add the new task
    new_task = {
        'id': get_next_id(data),
        'description': task,
        'status': 'to-do',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    data.append(new_task)
    # Save the JSON file
    with open('tasker.json', 'w') as f:
        json.dump(data, f, indent=4)
    print(f'Task "{task}" added successfully! (ID: {new_task["id"]})') 
    # Tabulate table
    print(tabulate(data, headers="keys", tablefmt="fancy_grid"))

# Delete a task
def delete_task(task_id, file_path):
    # Load the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)
    if not data:
        print('No tasks found!')
        #return
    else:
    # Find the task by ID
        length = len(data)
        for task in data:
            if task['id'] == task_id:
                data.remove(task)
                print(f'Task {task_id} deleted successfully!')
                break
            else:
                length -= 1
        # Tabulate table
        print(tabulate(data, headers="keys", tablefmt="fancy_grid"))
        if length == 0:
            print(f'Task {task_id} not found!')
    # Save the JSON file
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    
# Update a task
def update_task(task_id, task_update, file_path):
    # Load the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)
    if not data:
        print('No tasks found!')
        return
    # Find the task by ID
    length = len(data)
    for task in data:
        if task['id'] == task_id:
            task['description'] = task_update
            task['updated_at'] = datetime.now().isoformat()
            # Save the JSON file
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            print(f'Task {task_id} updated successfully!')
            break
        else:
            length -= 1
    # Tabulate table
    print(tabulate(data, headers="keys", tablefmt="fancy_grid"))
    if length == 0:
        print(f'Task {task_id} not found!')


# Mark a task as done
def mark_done(task_id, file_path):
    # Load the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)
    if not data:
        print('No tasks found!')
        return
    # Find the task by ID
    length = len(data)
    for task in data:
        if task['id'] == task_id:
            task['status'] = 'done'
            task['updated_at'] = datetime.now().isoformat()
            # Save the JSON file
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            print(f'Task {task_id} marked as done successfully!')
            break
        else:
            length -= 1
    # Tabulate table
    print(tabulate(data, headers="keys", tablefmt="fancy_grid"))
    if length == 0:
        print(f'Task {task_id} not found!')

# Mark a task as in progress
def mark_in_progress(task_id, file_path):
    # Load the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)
    if not data:
        print('No tasks found!')
        return
    # Find the task by ID
    length = len(data)
    for task in data:
        if task['id'] == task_id:
            task['status'] = 'in-progress'
            task['updated_at'] = datetime.now().isoformat()
            # Save the JSON file
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            print(f'Task {task_id} marked as in progress successfully!')
            break
        else:
            length -= 1
    # Tabulate table
    print(tabulate(data, headers="keys", tablefmt="fancy_grid"))
    if length == 0:
        print(f'Task {task_id} not found!')

# List tasks based on status
def list_tasks(status: Literal['to-do','in-progress','done'], file_path):
    # Load the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)
    if not data:
        print('No tasks found!')
        return 
    # Find the tasks by status
    length = len(data)
    ldata = []
    for task in data:
        if task['status'] == status:
            ldata.append(task)

        else:
            length -= 1
    # Tabulate table
    print(tabulate(ldata, headers="keys", tablefmt="fancy_grid"))
    if length == 0:
        print(f'No tasks found with status "{status}"!')

# Main function
def main():

    # Create the parser
    parser = create_parser()
    # Parse arguments
    args = parser.parse_args()
    
    # Execute the command
    commands = {
        'add': lambda: add_task(args.task_description, 'tasker.json'),
        'delete': lambda: delete_task(args.task_id, 'tasker.json'),
        'update': lambda: update_task(args.task_id, args.task_description, 'tasker.json'),
        'mark_done': lambda: mark_done(args.task_id, 'tasker.json'),
        'mark_in_progress': lambda: mark_in_progress(args.task_id, 'tasker.json'),
        'list': lambda: list_tasks(args.status, 'tasker.json'),
        'view': lambda: view_all_tasks(args.all, 'tasker.json')
    }
    if check_json('tasker.json'):
        command_function = commands.get(args.command)
        if command_function:
            command_function()
        else:
            parser.print_help()
    else:
        print('Please create a JSON file named "tasker.json" in the current directory.')
        return
if __name__ == '__main__':
    main()