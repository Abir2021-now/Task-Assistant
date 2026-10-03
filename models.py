class Task:

    def __init__(self, title, priority, completed=False):
        self.title = title
        self.priority = priority
        self.completed = completed

    def complete(self):
        self.completed = True

    def display(self):
        status = "Done" if self.completed else "Not done"
        return f"{self.title} | {self.priority} | {status}"
