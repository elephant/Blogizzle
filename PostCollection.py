from Post import Post

class PostCollection:
    """A collection of posts"""
    length = 0
    currentPage = 1
    totalPages = 1
    posts = []

    def __init__(self):
        self.length = 0
        self.currentPage = 1
        self.totalPages = 1
        self.posts = []

    def add(self, post):
        if isinstance(post, Post):
            self.posts.append(post)