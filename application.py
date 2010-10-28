import logging
from flask import Flask, render_template, request, url_for
from jinja2 import Markup
import markdown2

from Post import Post
from PostCollection import PostCollection
from PostDao import PostDao

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

def datetimeformat(value, format='%A, %B %d %I:%M %p %Z'):
    return value.strftime(format)

def markdown(value):
    return Markup(markdown2.markdown(value))

app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['markdown'] = markdown

@app.route('/')
def index():
    postDao = PostDao()
    posts = postDao.find()
    page = 1
    return render_template('index.html', posts = posts, page = page, nextPageUrl = url_for('page', page = page + 1), previousPageUrl = url_for('page', page = page - 1))

@app.route('/page<int:page>')
def page(page):
    postDao = PostDao()
    posts = postDao.find(page = page)
    return render_template('index.html', posts = posts, page = page, nextPageUrl = url_for('page', page = page + 1), previousPageUrl = url_for('page', page = page - 1))

@app.route('/post/new')
def postNew():
    return render_template('post/new.html')

@app.route('/post/save', methods=['POST'])
def postSave():
    formVals = request.form
    postDao = PostDao()
    post = Post(formVals)
    post.ensureDefaults()
    postDao.save(post)
    return render_template('post/save.html', formVals = formVals, post = post)

#errors
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404notFound.html')

if __name__ == '__main__':
    app.run()