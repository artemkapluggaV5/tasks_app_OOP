import sqlite3

DATABASE = "tasks.db"


# Шаг 1: Подготовка базы данных
def init_database():

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                priority TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


# Шаг 2: Загрузка задач из базы данных
def load_tasks():

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT id, title, priority FROM tasks ORDER BY created_at DESC")

        return cursor.fetchall()


# Шаг 3: Просмотр задач
def view_tasks():
    tasks = load_tasks()

    print("\n--- Список задач ---")
    if not tasks:
        print("Список задач пуст.")
    else:
        for task in tasks:
            print(f"{task[0]}. {task[1]} — [{task[2]}]")
    print("--------------------")


# Шаг 4: Добавление новой задачи
def add_task():
    title = input("Введите название задачи: ")
    priority = input("Введите приоритет (Низкий/Средний/Высокий): ")

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title, priority) VALUES (?, ?)", (title, priority))
        conn.commit()

    print("Задача успешно добавлена.")


# Шаг 5: Удаление задачи
def delete_task():
    view_tasks()

    try:
        task_id = int(input("Введите ID задачи для удаления: "))
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

        if cursor.rowcount == 0:
            print(f"Задача с ID {task_id} не найдена.")
        else:
            conn.commit()
            print("Задача удалена.")


# Шаг 6: Обновление задачи (Дополнительно)
def update_task():
    view_tasks()

    try:
        task_id = int(input("Введите ID задачи для обновления: "))
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return

    new_title = input("Введите новое название: ")
    new_priority = input("Введите новый приоритет: ")

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET title = ?, priority = ? WHERE id = ?",
            (new_title, new_priority, task_id)
        )

        if cursor.rowcount == 0:
            print(f"Задача с ID {task_id} не найдена, обновление невозможно.")
        else:
            conn.commit()
            print("Задача обновлена.")


# Шаг 7: Главное меню программы
def main():

    print("Добро пожаловать в менеджер задач с БД (SQLite)!")

    init_database()

    while True:
        print("\nМеню:")
        print("1 — Просмотреть задачи")
        print("2 — Добавить задачу")
        print("3 — Удалить задачу")
        print("4 — Обновить задачу")
        print("0 — Выход")

        choice = input("Выберите пункт меню: ")

        if choice == "1":
            view_tasks()
        elif choice == "2":
            add_task()
        elif choice == "3":
            delete_task()
        elif choice == "4":
            update_task()
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Ошибка: такого пункта меню нет. Попробуйте снова.")


if __name__ == "__main__":
    main()