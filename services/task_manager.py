from models.task import Task
import psycopg2


class TaskManager:


    def __init__(self, db):
        self.db = db

    def get_all_tasks(self):
        query = "SELECT id, title, priority, user_id, created_at FROM tasks ORDER BY created_at DESC"
        rows = self.db.fetchall(query)

        tasks = []
        for row in rows:

            task = Task(*row)
            tasks.append(task)

        return tasks

    def add_task(self):

        print("\n--- Добавление задачи ---")
        title = input("Введите название задачи: ")
        priority = input("Введите приоритет (Низкий/Средний/Высокий): ")

        try:
            user_id = int(input("Введите ID пользователя (1): "))
        except ValueError:
            print("Ошибка: ID пользователя должен быть числом.")
            return

        try:
            query = "INSERT INTO tasks (title, priority, user_id) VALUES (%s, %s, %s)"
            self.db.execute(query, (title, priority, user_id))
            print("Задача успешно добавлена.")
        except psycopg2.IntegrityError:
            print("Ошибка: Пользователь с таким ID не найден (Foreign Key Error).")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


    def delete_task(self):
        print("\n--- Удаление задачи ---")
        try:
            task_id = int(input("Введите ID задачи для удаления: "))
        except ValueError:
            print("Ошибка: ID должен быть числом.")
            return

        query = "DELETE FROM tasks WHERE id = %s"
        rows_deleted = self.db.execute(query, (task_id,))

        if rows_deleted > 0:
            print(f"Задача {task_id} удалена.")
        else:
            print(f"Задача с ID {task_id} не найдена.")

    def update_task(self):
        print("\n--- Обновление задачи ---")
        try:
            task_id = int(input("Введите ID задачи для обновления: "))
        except ValueError:
            print("Ошибка: ID должен быть числом.")
            return

        current_task = self.db.fetchone("SELECT * FROM tasks WHERE id = %s", (task_id,))
        if not current_task:
            print("Задача не найдена.")
            return

        new_title = input("Введите новое название: ")
        new_priority = input("Введите новый приоритет: ")

        query = """
                UPDATE tasks
                SET title = %s,
                priority = %s
                WHERE id = %s
                """

        self.db.execute(query, (new_title, new_priority, task_id))
        print("Задача обновлена.")