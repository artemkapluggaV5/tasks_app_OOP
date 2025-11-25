import psycopg2

CONNECT_DB = {
    'user': 'postgres',
    'password': 'admin',
    'host': 'localhost',
    'port': '5432',
    'database': 'tasks_app'
}


class Database:

    def __init__(self):
        self.config = CONNECT_DB

    def connect(self):
        return psycopg2.connect(**self.config)

    def create_tables(self):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                               CREATE TABLE IF NOT EXISTS users
                               (id SERIAL PRIMARY KEY,
                                   username TEXT UNIQUE NOT NULL,
                                   full_name TEXT,
                                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                               )
                               """)

                cursor.execute("""
                               CREATE TABLE IF NOT EXISTS tasks
                               (id SERIAL PRIMARY KEY,
                                   title TEXT NOT NULL,
                                   priority TEXT NOT NULL,
                                   user_id INTEGER,
                                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                   FOREIGN KEY (user_id)
                                   REFERENCES users(id)
                                   ON DELETE SET NULL)
                               """)


                cursor.execute("INSERT INTO users (username, full_name) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                               ('admin', 'adminovich'))

        print("База данных инициализирована.")

    def execute(self, query, params=()):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount

    def fetchall(self, query, params=()):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()

    def fetchone(self, query, params=()):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()