import logging
from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect, session
from jinja2 import Markup
import markdown2

from Post import Post
from PostCollection import PostCollection
from PostDao import PostDao

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)
app.secret_key = "\x81\x8e\xf7\xdbF\xc7\xc2\x89\xbd:\xdaW\x9e\x12\x8e\xb2\x14\xf0\x14\xde\x08\x0e\x9a\x82"

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
    if page < 2:
        return redirect(url_for('index'), 301)
    else:
      postDao = PostDao()
      posts = postDao.find(page = page)
      if page > posts.totalPages:
        return redirect(url_for('index'), 301)
      else:
        return render_template('index.html', posts = posts, page = page, nextPageUrl = url_for('page', page = page + 1), previousPageUrl = url_for('page', page = page - 1))

@app.route('/post/new')
def postNew():
    today = datetime.today()
    return render_template('post/new.html', today = today)

@app.route('/post/save', methods=['POST'])
def postSave():
    app.open_session(request)
    formVals = request.form
    session['email'] = formVals['email']
    session['author'] = formVals['author']
    postDao = PostDao()
    post = Post(formVals)
    post.ensureDefaults()
    postDao.save(post)
    return render_template('post/save.html', formVals = formVals, post = post)

#errors
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404notFound.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('error/404notFound.html'), 404

if __name__ == '__main__':
    app.run()