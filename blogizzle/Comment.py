from datetime import datetime

from mongoengine import DateTimeField, EmbeddedDocument, StringField, URLField

class Comment(EmbeddedDocument):
    """A comment"""
    body = StringField(required=True)
    ip = StringField(required=True, regex="\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    publishTime = DateTimeField(default=datetime.now)
    slug = URLField()