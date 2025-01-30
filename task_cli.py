#!/usr/local/bin/python3
import os
import json
import argparse
from datetime import datetime

TASKS_FILE = 'tasks.json'

# Load tasks from JSON file


def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    return []

# Save tasks to JSON file


def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# Function to generate task ID


def generate_id(tasks):
    return max([task['id'] for task in tasks], default=0) + 1


def add_task(description):
    tasks = load_tasks()
    task_id = generate_id(tasks)
    task = {
        'id': task_id,
        'description': description,
        'status': 'todo',
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat(),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")


def update_task(task_id, new_description):
    tasks = load_tasks()
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        task['description'] = new_description
        task['updatedAt'] = datetime.now().isoformat()
        save_tasks(tasks)
        print(f"Task {task_id} updated successfully.")
    else:
        print(f"Task with ID {task_id} not found.")


def delete_task(task_id):
    tasks = load_tasks()
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        tasks = [task for task in tasks if task['id'] != task_id]
        save_tasks(tasks)
        print(f"Task {task_id} deleted successfully.")
    else:
        print(f"Task with ID {task_id} not found.")


def mark_task_status(task_id, status):
    if status not in ['todo', 'in-progress', 'done']:
        print("Invalid status. Use 'todo', 'in-progress', or 'done'.")
        return
    tasks = load_tasks()
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        task['status'] = status
        task['updatedAt'] = datetime.now().isoformat()
        save_tasks(tasks)
        print(f"Task {task_id} marked as {status}.")
    else:
        print(f"Task with ID {task_id} not found.")


def list_tasks(status=None):
    tasks = load_tasks()
    if status:
        filtered_tasks = [task for task in tasks if task['status'] == status]
    else:
        filtered_tasks = tasks
    for task in filtered_tasks:
        print(f"ID: {task['id']}, Description: {
              task['description']}, Status: {task['status']}")


def main():
    parser = argparse.ArgumentParser(description='Task Tracker CLI')
    subparsers = parser.add_subparsers(dest='command')

    # Add task
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('description', type=str, help='Task description')

    # Update task
    update_parser = subparsers.add_parser(
        'update', help='Update an existing task')
    update_parser.add_argument('id', type=int, help='Task ID')
    update_parser.add_argument(
        'description', type=str, help='New task description')

    # Delete task
    delete_parser = subparsers.add_parser(
        'delete', help='Delete an existing task')
    delete_parser.add_argument('id', type=int, help='Task ID')

    # Mark task as in progress
    mark_in_progress_parser = subparsers.add_parser(
        'mark-in-progress', help='Mark a task as in-progress')
    mark_in_progress_parser.add_argument('id', type=int, help='Task ID')

    # Mark task as done
    mark_done_parser = subparsers.add_parser(
        'mark-done', help='Mark a task as done')
    mark_done_parser.add_argument('id', type=int, help='Task ID')

    # List tasks (all or by status)
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument(
        'status', type=str, choices=['todo', 'in-progress', 'done'], nargs='?',
        help='Filter tasks by status (optional)'
    )

    args = parser.parse_args()

    if args.command == 'add':
        add_task(args.description)
    elif args.command == 'update':
        update_task(args.id, args.description)
    elif args.command == 'delete':
        delete_task(args.id)
    elif args.command == 'mark-in-progress':
        mark_task_status(args.id, 'in-progress')
    elif args.command == 'mark-done':
        mark_task_status(args.id, 'done')
    elif args.command == 'list':
        # None if no status, otherwise filter by status
        list_tasks(args.status)


if __name__ == '__main__':
    main()
