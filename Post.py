from datetime import datetime

from CommentCollection import CommentCollection

class Post:
    """A post"""
    title = ""
    body = ""
    author = ""
    email = ""
    ip = ""
    publishTime = ""
    publishDay = ""
    slug = ""
    comments = CommentCollection()
    commentCount = 0

    def __init__(self, dictionary = ""):
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
            if 'commentCount' in dictionary:
                self.commentCount = int(dictionary['commentCount'])
            if 'publishTime' in dictionary:
                try:
                    if isinstance(dictionary['publishTime'], unicode) or isinstance(dictionary['publishTime'], str):
                        self.publishTime = datetime.strptime(dictionary['publishTime'], "%Y-%m-%d")
                    else:
                        self.publishTime = dictionary['publishTime']
                except:
                    self.publishTime = datetime.today()
            self.publishDay = int(self.publishTime.strftime("%Y%m%d"))
            self.slug = self.publishTime.strftime("%Y.%b") + "-" + self.title.lower().replace(" ", "-")
            if 'comments' in dictionary:
                del self.comments[:]
                self.comments.appendAll(dictionary['comments'])
            else:
                self.comments = CommentCollection()
        else:
            self.title = ""
            self.body = ""
            self.author = ""
            self.email = ""
            self.ip = ""
            self.publishTime = datetime.today()
            self.publishDay = self.publishTime.strftime("%Y%m%d")
            self.slug = ""
            self.comments = CommentCollection()
            self.commentCount = 0

    def ensureDefaults(self):
        if self.publishTime == "":
            self.publishTime = datetime.today()