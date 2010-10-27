from datetime import datetime

class Post:
    """A post"""
    title = ""
    body = ""
    author = ""
    email = ""
    ip = ""
    publishTime = ""

    def __init__(self):
        self.title = ""
        self.body = ""
        self.author = ""
        self.email = ""
        self.ip = ""
        self.publishTime = datetime.today()

    def __init__(self, dictionary):
        if isinstance(dictionary, dict):
            if 'title' in dictionary:
                self.title = dictionary['title']
            if 'body' in dictionary:
                self.body = dictionary['body']
            if 'author' in dictionary:
                self.author = dictionary['author']
            if 'email' in dictionary:
                self.email = dictionary['email']
            if 'ip' in dictionary:
                self.ip = dictionary['ip']
            if 'publishTime' in dictionary:
                try:
                    if isinstance(dictionary['publishTime'], unicode) or isinstance(dictionary['publishTime'], str):
                        self.publishTime = datetime.strptime(dictionary['publishTime'], "%Y-%m-%d")
                    else:
                        self.publishTime = dictionary['publishTime']
                except:
                    self.publishTime = datetime.today()

    def ensureDefaults(self):
        if self.publishTime == "":
            self.publishTime = datetime.today()