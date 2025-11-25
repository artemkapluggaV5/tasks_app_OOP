from services.database import Database
from services.task_manager import TaskManager


class App:

    def __init__(self):
        self.db = Database()
        self.db.create_tables()
        self.manager = TaskManager(self.db)

    def run(self):
        print("Добро пожаловать в объектно-ориентированный менеджер задач!")

        while True:
            print("\nМеню:")
            print("1 — Просмотреть задачи")
            print("2 — Добавить задачу")
            print("3 — Удалить задачу")
            print("4 — Обновить задачу")
            print("0 — Выход")

            choice = input("Выберите пункт меню: ")

            if choice == "1":
                tasks = self.manager.get_all_tasks()
                print("\n--- Список задач ---")
                if not tasks:
                    print("Список пуст.")
                else:
                    for t in tasks:
                        print(t)
                print("--------------------")

            elif choice == "2":
                self.manager.add_task()

            elif choice == "3":
                self.manager.delete_task()

            elif choice == "4":
                self.manager.update_task()


            elif choice == "0":
                print("Выход из программы.")
                break

            else:
                print("Ошибка: такого пункта меню нет.")


if __name__ == "__main__":
    app = App()
    app.run()