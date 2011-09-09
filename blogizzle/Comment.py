from datetime import datetime

class Comment:
    """A comment"""
    body = ""
    author = ""
    email = ""
    ip = ""
    publishTime = ""
    slug = ""

    def __init__(self, dictionary = ""):
        self.ensureDefaults()
        if isinstance(dictionary, dict):
            if 'body' in dictionary:
                self.body = dictionary['body']
            if 'author' in dictionary:
                self.author = dictionary['author']
            if 'email' in dictionary:
                self.email = dictionary['email']
            if 'ip' in dictionary:
                self.ip = dictionary['ip']
            if 'publishTime' in dictionary:
                self.publishTime = dictionary['publishTime']
        else:
            self.body = ""
            self.author = ""
            self.email = ""
            self.ip = ""
            self.publishTime = datetime.today()

    def ensureDefaults(self):
        if self.publishTime == "":
            self.publishTime = datetime.today()