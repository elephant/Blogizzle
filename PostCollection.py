from Post import Post

class PostCollection(list):
    """A collection of posts"""
    length = 0
    currentPage = 1
    totalPages = 1

    def __init__(self):
        self.length = 0
        self.currentPage = 1
        self.totalPages = 1

    def append(self, post):
        if isinstance(post, dict):
            post = Post(post)
        if isinstance(post, Post):
            list.append(self, post)
            self.length += 1