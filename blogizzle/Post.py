from datetime import datetime

from mongoengine import DateTimeField, Document, EmbeddedDocumentField, IntField, ObjectIdField, SortedListField, StringField, URLField

from Comment import Comment

class Post(Document):
    """A post"""
    _id = ObjectIdField()
    title = StringField(required=True)
    body = StringField(required=True)
    ip = StringField(required=True, regex="\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    publish_time = DateTimeField(default=datetime.now)
    publish_day = IntField(required=True) #YYYYMMDD used for quick searching/cache optimization
    slug = StringField(required=True, unique=True)
    #comments = SortedListField(EmbeddedDocumentField(Comment))
    comment_count = IntField(min_value=0)

    def init_from_dict(self, dictionary):
        if dictionary is not None and isinstance(dictionary, dict):
            if 'title' in dictionary:
                self.title = dictionary['title']
            if 'body' in dictionary:
                self.body = dictionary['body']

    def addComment(self, comment):
        if isinstance(comment, Comment):
            self.comments.append(comment)
            comment_count += 1 #({"slug": slug}, {"$push": {"comments": comment}, "$inc": {"comment_count": 1}})

    def save(self, safe=True, force_insert=False, validate=True):
        if self.publish_time is None:
            self.publish_time = datetime.now
        if self.slug is None:
            self.slug = self.publish_time.strftime("%Y.%b") + "-" + self.title.lower().replace(" ", "-")
        if self.publish_day is None:
            self.publish_day = int(self.publish_time.strftime("%Y%m%d"))
        Document.save(self, safe=safe, force_insert=force_insert, validate=validate)

    @staticmethod
    def posts_by_page(page = 1, posts_per_page = 5):
        """Get a set of posts by page number, starting with 1"""
        page = page - 1 #convert to 0 based index
        start = page * posts_per_page
        end = start + posts_per_page
        return Post.objects[start:end]

    @staticmethod
    def total_pages(posts_per_page = 5):
        return len(Post.objects) / (posts_per_page + (posts_per_page % posts_per_page))