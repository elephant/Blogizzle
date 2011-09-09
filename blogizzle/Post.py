from datetime import datetime

from mongoengine import DateTimeField, Document, EmbeddedDocumentField, IntField, ObjectIdField, SortedListField, StringField, URLField

from Comment import Comment

class Post(Document):
    """A post"""
    _id = ObjectIdField()
    title = StringField(required=True)
    body = StringField(required=True)
    ip = StringField(required=True, regex="\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    publishTime = DateTimeField(default=datetime.now)
    publishDay = IntField(required=True) #YYYYMMDD used for quick searching/cache optimization
    slug = StringField(required=True, unique=True)
    #comments = SortedListField(EmbeddedDocumentField(Comment))
    commentCount = IntField(min_value=0)

    def addComment(self, comment):
        if isinstance(comment, Comment):
            self.comments.append(comment)
            commentCount += 1 #({"slug": slug}, {"$push": {"comments": comment}, "$inc": {"commentCount": 1}})

    def save(self, safe=True, force_insert=False, validate=True):
        if self.publishTime is None:
            self.publishTime = datetime.now
        if self.slug is None:
            self.slug = self.publishTime.strftime("%Y.%b") + "-" + self.title.lower().replace(" ", "-")
        if self.publishDay is None:
            self.publishDay = int(self.publishTime.strftime("%Y%m%d"))
        Document.save(self, safe=safe, force_insert=force_insert, validate=validate)