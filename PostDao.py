import math

import pymongo

from Comment import Comment
from CommentCollection import CommentCollection
from Post import Post
from PostCollection import PostCollection

class PostDao:
    """Retrieve posts"""

    def __init__(self):
        self.connection = pymongo.Connection() 
        self.db = self.connection.blogizzle
    
    def __del__(self):
        self.connection.disconnect()

    def save(self, post):
        self.db.posts.save(post.__dict__)

    def saveComment(self, comment, slug):
        self.db.posts.update({"slug": slug}, {"$push": {"comments": comment.__dict__}, "$inc": {"commentCount": 1}})

    def findOne(self, slug = ""):
        post = Post(self.db.posts.find_one({"slug": slug}))
        return post

    def find(self, limit = 5, page = 1):
        fields = ['author', 'body', 'email', 'publishTime', 'slug', 'title', 'commentCount']
        mongoPosts = self.db.posts.find(limit = limit, skip = (limit * (page - 1)), fields = fields).sort("publishTime", -1)
        posts = PostCollection()
        posts.length = mongoPosts.count()
        posts.currentPage = page
        if posts.length > limit:
            posts.totalPages = (posts.length / limit) + (posts.length % limit)
        else:
            posts.totalPages = 1

        for mongoPost in mongoPosts:
            post = Post(mongoPost)
            posts.append(post)
        return posts