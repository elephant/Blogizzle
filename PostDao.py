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

    def find(self, limit):
        self.connect()
        mongoPosts = self.db.posts.find(limit = limit)
        posts = []
        for mongoPost in mongoPosts:
            post = Post(mongoPost)
            posts.append(post)
        return posts