import sys
import json
import os
from datetime import datetime


def load_tasks():
    if not os.path.exists("tasks.json"):
        return []

    with open("tasks.json", "r") as file:
        return json.load(file)


def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)



def add_task(description):
    tasks = load_tasks()

    new_task = {
        "id": len(tasks) + 1,
        "description": description,
        "status": "todo",
        "createdAt": str(datetime.now()),
        "updatedAt": str(datetime.now())
    }

    tasks.append(new_task)
    save_tasks(tasks)

    print(f"Tarefa adicionada com sucesso (ID: {new_task['id']})")


def list_tasks(filter_status=None):
    tasks = load_tasks()

    if filter_status:
        tasks = [t for t in tasks if t["status"] == filter_status]

    if not tasks:
        print("Nenhuma tarefa encontrada.")
        return

    for task in tasks:
        print(f"{task['id']} - {task['description']} [{task['status']}]")

        
def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]

    if len(tasks) == len(new_tasks):
        print("ID não encontrado.")
        return

    save_tasks(new_tasks)
    print("Tarefa deletada com sucesso!")


def update_task(task_id, new_description):
    tasks = load_tasks()
    found = False

    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = str(datetime.now())
            found = True

    if not found:
        print("ID não encontrado.")
        return

    save_tasks(tasks)
    print("Tarefa atualizada com sucesso!")


def mark_status(task_id, status):
    tasks = load_tasks()
    found = False

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = str(datetime.now())
            found = True

    if not found:
        print("ID não encontrado.")
        return

    save_tasks(tasks)
    print(f"Tarefa marcada como {status}!")


def main():
    args = sys.argv

    if len(args) < 2:
        print("Use um comando: add, list, update, delete...")
        return

    command = args[1]

    try:
        if command == "add":
            add_task(args[2])

        elif command == "list":
            if len(args) == 3:
                list_tasks(args[2])
            else:
                list_tasks()

        elif command == "delete":
            delete_task(int(args[2]))

        elif command == "update":
            update_task(int(args[2]), args[3])

        elif command == "mark-done":
            mark_status(int(args[2]), "done")

        elif command == "mark-in-progress":
            mark_status(int(args[2]), "in-progress")

        else:
            print("Comando inválido.")

    except IndexError:
        print("Argumentos faltando. Verifique o comando.")
    except ValueError:
        print("ID deve ser um número.")


if __name__ == "__main__":
    main()
