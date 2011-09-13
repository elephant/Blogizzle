import logging
import re
from datetime import datetime
from hashlib import md5

from flask import Flask, render_template, request, url_for, redirect, session, g, flash
from jinja2 import Markup, environmentfilter, evalcontextfilter
import markdown

from mongoengine import connect

from blogizzle.Post import Post
from blogizzle.Comment import Comment

app = Flask(__name__)
app.secret_key = "\x81\x8e\xf7\xdbF\xc7\xc2\x89\xbd:\xdaW\x9e\x12\x8e\xb2\x14\xf0\x14\xde\x08\x0e\x9a\x82"

########## Routes
@app.route('/')
def index():
    posts = Post.objects
    page = 1
    return render_template('index.html', posts = posts, page = page, total_pages = Post.total_pages, nextPageUrl = url_for('page', page = page + 1), previousPageUrl = url_for('page', page = page - 1))

@app.route('/page<int:page>')
def page(page):
    if page < 2:
        return redirect(url_for('index'), 301)
    else:
      if page > Post.total_pages:
        return redirect(url_for('index'), 301)
      else:
        posts = Post.posts_by_page(page)
        return render_template('index.html', posts = posts, page = page, total_pages = posts.total_pages, nextPageUrl = url_for('page', page = page + 1), previousPageUrl = url_for('page', page = page - 1))

@app.route('/<slug>.html', methods=['GET'])
def read(slug):
    comment = Comment()
    post = Post.objects(slug = slug)
    return render_template('post.html', post = post, comment = comment)

@app.route('/<slug>.html', methods=['POST'])
def commentSave(slug):
    app.open_session(request)
    formVals = request.form
    comment = Comment(formVals)
    comment.body = Markup(comment.body).striptags()

    if formVals['email'] and formVals['author'] and formVals['body'] and len(formVals['body']) > 10:
        emailRegex = re.compile("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(?:[a-zA-Z]{2}|com|org|net|edu|gov|mil|biz|info|mobi|name|aero|asia|jobs|museum)$")
        if emailRegex.match(formVals['email']):
            session['email'] = formVals['email']
            session['author'] = formVals['author']
            comment.ensureDefaults()
            g.postDao.saveComment(comment, slug)
            comment.body = ""
        else:
            flash("The email address you entered, '%s', is invalid." % formVals['email'], category='error')
    else:
        flash("You must enter your name, email address, and some text to post a comment.", category='error')
    post = g.postDao.findOne(slug)
    return render_template('post.html', post = post, comment = comment)

@app.route('/post')
def postNew():
    today = datetime.today()
    return render_template('post/new.html', today = today)

@app.route('/post', methods=['POST'])
def postSave():
    app.open_session(request)
    post = Post(request.form)
    try:
        post.save(post)
        flash("Saved")
        return redirect(url_for('read', slug = post.slug))
    except:
        flash("Uh oh", category = "error")
        return render_template('post.html', post = post)

########## Common Application Functionality
#errors
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404notFound.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('error/404notFound.html'), 404

#request
@app.before_request
def before_request():
    """Setup some common daos so we can use them across the board"""
    g.connect = connect('blogizzle')

@app.after_request
def after_request(response):
    """Destroy the daos."""
    del(g.connect)
    return response

########## Custom Jinja2 Filters
def datetimeformat(value, format='%A, %B %d %I:%M %p %Z'):
    return value.strftime(format)

def markdown2html(value):
    return Markup(markdown.markdown(value))

def gravatar(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)

app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['markdown2html'] = markdown2html
app.jinja_env.filters['gravatar'] = gravatar


########## Debug app - local development server
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)
    app.debug = True
    app.run()