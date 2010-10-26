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
        mongoPost = self.db.posts.find_one()
        return self.mapDictToObject(mongoPost)

    def find(self, limit):
        self.connect()
        mongoPosts = self.db.posts.find(limit = limit)
        posts = []
        for mongoPost in mongoPosts:
            posts.append(self.mapDictToObject(mongoPost))
        return posts

    def mapDictToObject(self, dict):
        post = Post()
        print dict
        try:
            if 'title' in dict:
                post.title = dict['title']
            if 'body' in dict:
                post.body = dict['body']
            if 'author' in dict:
                post.author = dict['author']
            if 'email' in dict:
                post.email = dict['email']
            if 'ip' in dict:
                post.ip = dict['ip']
            if 'publishTime' in dict:
                if isinstance(dict['publishTime'], unicode) or isinstance(dict['publishTime'], str):
                    post.publishTime = datetime.strptime(dict['publishTime'], "%Y-%m-%d")
                else:
                    post.publishTime = dict['publishTime']
            print dict['publishTime'].__class__
        except:
            post = Post()
        return post