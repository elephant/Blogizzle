import math

import pymongo

from Post import Post
from PostCollection import PostCollection

class PostDao:
    """Retrieve posts"""

    def __init__(self):
        pass

    def connect(self):
        self.connection = pymongo.Connection()
        self.db = self.connection.blogizzle

    def save(self, post):
        self.connect()
        self.db.posts.save(post.__dict__)

    def findOne(self):
        self.connect()
        post = Post(self.db.posts.find_one())
        return post

    def find(self, limit = 5, page = 1):
        self.connect()
        mongoPosts = self.db.posts.find(limit = limit, skip = (limit * (page - 1)))
        posts = PostCollection()
        posts.length = mongoPosts.count()
        posts.currentPage = page
        posts.totalPages = (posts.length / limit) + (posts.length % limit)
        for mongoPost in mongoPosts:
            post = Post(mongoPost)
            posts.add(post)
        return posts