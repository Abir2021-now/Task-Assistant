import database


def add_task():
    title = input("Enter a task: ").strip()

    if not title:
        print("Task title cannot be empty.")
        return

    while True:
        priority = input("Enter priority (high/medium/low): ")

        if priority in ["high", "medium", "low"]:
            break

        print("Invalid priority.")

    database.create_task(title, priority)

    print("Task added!")


def view_tasks():
    tasks = database.get_tasks()

    print("\nYour tasks:")

    if not tasks:
        print("No tasks yet.")
        return

    for task in tasks:
        task_id = task[0]
        title = task[1]
        priority = task[2]
        completed = task[3]

        status = "Done" if completed else "Not done"

        print(f"{task_id}. {title} | {priority} | {status}")


def mark_complete():
    task_id = input("Enter task ID to complete: ")

    if not task_id.isdigit():
        print("Task ID must be a number.")
        return

    updated = database.complete_task(int(task_id))

    if updated:
        print("Task completed!")
    else:
        print("Task not found.")


def remove_task():
    task_id = input("Enter task ID to delete: ")

    if not task_id.isdigit():
        print("Task ID must be a number.")
        return

    deleted = database.delete_task(int(task_id))

    if deleted:
        print("Task deleted!")
    else:
        print("Task not found.")


database.initialize_database()


while True:
    print("\n===== Task Assistant =====")
    print("1. Add task")
    print("2. View tasks")
    print("3. Complete task")
    print("4. Delete task")
    print("5. Exit")

    choice = input("Choose: ")

    if choice == "1":
        add_task()

    elif choice == "2":
        view_tasks()

    elif choice == "3":
        mark_complete()

    elif choice == "4":
        remove_task()

    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")
