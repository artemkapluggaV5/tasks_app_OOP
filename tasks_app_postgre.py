import psycopg2
import os

# ЛЕЧИМ КОДИРОВКУ НА WINDOWS:
os.environ["PGCLIENTENCODING"] = "utf-8"

DATABASE = 'tasks_app.db'

CONNECT_DB = {
    'user': 'postgres',
    'password': '123',
    'host': 'localhost',
    'port': '5432',
    'database': 'tasks_app'
}

def init_database():
    with psycopg2.connect(**CONNECT_DB) as conn:
        cursor = conn.cursor()

        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS priorities (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL UNIQUE
                    )
                """)
        cursor.executemany("INSERT INTO priorities (name) VALUES (%s) ON CONFLICT DO NOTHING",
                           [('Низкий',), ('Средний',), ('Высокий',)])


        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id SERIAL PRIMARY KEY,
                        title TEXT NOT NULL,
                        priority_id INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (priority_id) REFERENCES priorities (id)
                    )
                """)
        conn.commit()


def load_tasks():
    with psycopg2.connect(**CONNECT_DB) as conn:
        cursor = conn.cursor()

        query = """
                   SELECT tasks.id, tasks.title, priorities.name 
                   FROM tasks 
                   JOIN priorities ON tasks.priority_id = priorities.id 
                   ORDER BY tasks.created_at DESC
               """
        cursor.execute(query)

        return cursor.fetchall()

def view_tasks():
    tasks = load_tasks()

    print("\n--- Список задач ---")
    if not tasks:
        print("Список задач пуст.")
    else:
        for task in tasks:
            print(f"{task[0]}. {task[1]} — [{task[2]}]")
    print("--------------------")


def add_task():
    title = input("Введите название задачи: ")
    priority = input("Введите приоритет (Низкий/Средний/Высокий): ")

    with psycopg2.connect(**CONNECT_DB) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                        INSERT INTO tasks (title, priority_id) 
                        VALUES (%s, (SELECT id FROM priorities WHERE name = %s))
                    """, (title, priority))

            conn.commit()
            print("Задача успешно добавлена.")

        except psycopg2.IntegrityError:
            print(f"Ошибка: Приоритета '{priority}' нет в базе. Используйте: Низкий, Средний, Высокий.")

def delete_task():
        view_tasks()

        try:
            task_id = int(input("Введите ID задачи для удаления: "))
        except ValueError:
                print("Ошибка: ID должен быть числом.")
                return

        with psycopg2.connect(**CONNECT_DB) as conn:
            cursor = conn.cursor()

            cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))

            if cursor.rowcount == 0:
                        print(f"Задача с ID {task_id} не найдена.")
            else:
                        conn.commit()
                        print("Задача удалена.")


def update_task():
    view_tasks()

    try:
        task_id = int(input("Введите ID задачи для обновления: "))
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return

    new_title = input("Введите новое название: ")
    new_priority = input("Введите новый приоритет: ")

    with psycopg2.connect(**CONNECT_DB) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                        UPDATE tasks 
                        SET title = %s, 
                            priority_id = (SELECT id FROM priorities WHERE name = %s) 
                        WHERE id = %s
                    """, (new_title, new_priority, task_id))

            if cursor.rowcount == 0:
                print(f"Задача с ID {task_id} не найдена.")
            else:
                conn.commit()
                print("Задача обновлена.")

        except psycopg2.IntegrityError:
            print(f"Ошибка: Приоритета '{new_priority}' нет в базе.")


def main():

    print("Добро пожаловать в менеджер задач с БД (PostgreSQL)!")

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