import argparse
from datetime import datetime
import json
import os

def create_parser():
    # main parser
    parser = argparse.ArgumentParser(prog='Tasker', description='"Tasker" a simple task manager')
    # subparsers for different commands
    subparsers = parser.add_subparsers(dest='command',help='sub-command help')
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

# Generate the next numeric ID based on the existing tasks.
def get_next_id(tasks):
    if not tasks:
        return 1  # Start from 1 if no tasks exist
    return max(task["id"] for task in tasks) + 1

# Methods to handle the arguments
# Add a task
def add_task(task, file_path):
    # Load the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)
    # Add the new task
    new_task = {
        'id': get_next_id(data),
        'description': task,
        'status': 'to do',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    data.append(new_task)
    # Save the JSON file
    with open('tasker.json', 'w') as f:
        json.dump(data, f, indent=4)
    print(f'Task "{task}" added successfully! (ID: {new_task["id"]})') 

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
        for task in data:
          if task['id'] == task_id:
                data.remove(task)
                print(f'Task {task_id} deleted successfully!')
                break
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
    if length == 0:
        print(f'Task {task_id} not found!')


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
        'mark_done': lambda: mark_done(args.task_id, 'tasker.json')
    }
    if check_json('tasker.json'):
        command_function = commands.get(args.command)
        if command_function:
            command_function()
        else:
            parser.print_help()

if __name__ == '__main__':
    main()