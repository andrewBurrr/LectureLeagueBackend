

class Course:
    def __init__(self, title, code, number, topic, description, subtopics, parent):
        self.title = title
        self.code = code
        self.number = number
        self.topic = topic
        self.description = description
        self.subtopics = subtopics
        self.parent = parent

    def __str__(self):
        return f"{self.title} {self.code} {self.number} | {self.description}"
