import math
from datetime import datetime

from mongoengine import DateTimeField, Document, EmbeddedDocumentField, IntField, ObjectIdField, SortedListField, StringField, URLField

__all__ = ['Post']

class Post(Document):
    """A post"""
    meta = {
        'index_drop_dups': True,
        'index_background': True,
        'indexes': [
            'slug',
            'publish_time'
        ],
        'ordering': ['-publish_time']
    }
    title = StringField(required = True, min_length = 1, max_length = 50)
    body = StringField(required = True, min_length = 1)
    ip = StringField(required = True, regex = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    publish_time = DateTimeField(required = True)
    publish_day = IntField(required = True) #YYYYMMDD used for quick searching/cache optimization
    slug = StringField(required = True, unique = True)
    #comments = SortedListField(EmbeddedDocumentField(Comment))
    comment_count = IntField(min_value = 0, default = 0)

    def init_from_dict(self, dictionary):
        if dictionary is not None and isinstance(dictionary, dict):
            if 'title' in dictionary:
                self.title = dictionary['title']
            if 'body' in dictionary:
                self.body = dictionary['body']

    def save(self, safe=True, force_insert=False, validate=True):
        if self.publish_time is None:
            self.publish_time = datetime.now()
        if self.slug is None:
            self.slug = self.publish_time.strftime("%Y.%b") + "-" + self.title.lower().replace(" ", "-")
        if self.publish_day is None:
            self.publish_day = int(self.publish_time.strftime("%Y%m%d"))
        Document.save(self, safe=safe, force_insert=force_insert, validate=validate)

    def posts_after_this(self):
        #the ordering looks odd, but that's because we're displaying posts in descending order
        return Post.objects(__raw__ = {"_id":{"$lt": self.id }})

    def posts_before_this(self):
        #the ordering looks odd, but that's because we're displaying posts in descending order
        return Post.objects(__raw__ = {"_id":{"$gt": self.id }}).order_by('publish_time')

    def next_post(self):
        next_post = self.posts_after_this()
        if len(next_post) > 0:
            return next_post[0]
        return None

    def previous_post(self):
        previous_post = self.posts_before_this()
        if len(previous_post) > 0:
            return previous_post[0]
        return None

    @staticmethod
    def posts_by_page(page = 1, posts_per_page = 1):
        """Get a set of posts by page number, starting with 1"""
        page = page - 1 #convert to 0 based index
        start = page * posts_per_page
        end = start + posts_per_page
        return Post.objects[start:end].order_by('-publish_time')

    @staticmethod
    def total_pages(posts_per_page = 1):
        return int(math.ceil(len(Post.objects) / float(posts_per_page)))
