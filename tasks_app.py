import os
import json

FILENAME = "tasks.json"

def load_tasks():
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w", encoding="utf-8") as f:
            json.dump([], f)
        print("Файл не найден, создан новый пустой файл.")
        return []

    with open(FILENAME, "r", encoding="utf-8") as f:
        try:
            tasks = json.load(f)
            return tasks
        except json.JSONDecodeError:
            print("Файл пустой или поврежден. Возвращаем пустой список.")
            return []

def save_tasks(tasks):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

def view_tasks(tasks):
    if not tasks:
        print("Список задач пуст.")
        return
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task['title']} — [{task['priority']}]")

def add_task(tasks):
    title = input("Введите название задачи: ")
    priority = input("Введите приоритет (Низкий/Средний/Высокий): ")
    task = {"title": title, "priority": priority}
    tasks.append(task)
    save_tasks(tasks)
    print("Задача добавлена.")

def delete_task(tasks):
    if not tasks:
        print("Нет задач для удаления.")
        return

    view_tasks(tasks)
    number = input("Введите номер задачи для удаления: ")

    try:
        num = int(number)
    except ValueError:
        print("Некорректный ввод. Введите число.")
        return

    if num < 1 or num > len(tasks):
        print("Некорректный номер задачи.")
        return

    removed_task = tasks.pop(num - 1)
    save_tasks(tasks)
    print(f"Задача '{removed_task['title']}' удалена.")


def main():
    print("Добро пожаловать в менеджер задач!")
    tasks = load_tasks()

    while True:
        print("\nМеню:")
        print("1 — Просмотреть задачи")
        print("2 — Добавить задачу")
        print("3 — Удалить задачу")
        print("0 — Выход")

        choice = input("Выберите пункт меню: ")

        if choice == "1":
            view_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Ошибка: такого пункта меню нет. Попробуйте снова.")


if __name__ == "__main__":
    main()
