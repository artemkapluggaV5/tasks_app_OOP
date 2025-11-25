class User:

    def __init__(self, id, username, full_name, created_at):
        self.id = id
        self.username = username
        self.full_name = full_name
        self.created_at = created_at

    def __str__(self):
        return f"User {self.id}: {self.username} ({self.full_name})"