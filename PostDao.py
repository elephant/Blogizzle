from datetime import datetime
import pymongo
from pymongo import Connection
from Post import Post

class PostDao:
    """Retrieve posts"""

    def __init__(self):
        pass

    def connect(self):
        self.connection = Connection()
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
        posts = []
        for mongoPost in mongoPosts:
            post = Post(mongoPost)
            posts.append(post)
        return posts