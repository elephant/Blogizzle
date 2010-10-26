from datetime import datetime

class Post:
    """A post"""
    test = ""

    def __init__(self):
        self.title = ""
        self.body = ""
        self.author = ""
        self.email = ""
        self.ip = ""
        self.publishTime = datetime.today()