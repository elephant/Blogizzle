from Comment import Comment

class CommentCollection(list):
    """A collection of comments"""
    length = 0

    def __init__(self):
        self.length = 0

    def append(self, comment):
        if isinstance(comment, dict):
            comment = Comment(comment)
        if isinstance(comment, Comment):
            list.append(self, comment)
            self.length += 1

    def appendAll(self, commentList):
        if isinstance(commentList, list):
            for comment in commentList:
                self.append(comment)