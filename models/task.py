class Task:

    def __init__(self, id, title, priority, user_id, created_at):
        self.id = id
        self.title = title
        self.priority = priority
        self.user_id = user_id
        self.created_at = created_at

    def __str__(self):
        return f"{self.id}. {self.title} — [{self.priority}] (User ID: {self.user_id})"