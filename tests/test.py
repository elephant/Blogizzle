from blogizzle.Post import Post

from mongoengine import connect

connect('blogizzle', host='Hippo.local')

post = Post(title="Hello World!",
            body="Blah blah blah",
            ip="127.0.0.1")

try:
    post.save()
except:
    post._id = Post.objects(slug=post.slug).first()._id
    post.save()