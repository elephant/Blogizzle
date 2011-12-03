import datetime
import hashlib
import logging
import re
#from datetime import datetime

import flask
import jinja2
import mongoengine
import markdown

from blogizzle.Post import Post

app = flask.Flask(__name__)
app.secret_key = "\x81\x8e\xf7\xdbF\xc7\xc2\x89\xbd:\xdaW\x9e\x12\x8e\xb2\x14\xf0\x14\xde\x08\x0e\x9a\x82"

########## Routes
@app.route('/')
def index():
    page = 1
    posts = Post.posts_by_page(page)
    total_pages = Post.total_pages()
    return flask.render_template('index.html', posts = posts, page = page, total_pages = total_pages, nextPageUrl = flask.url_for('page', page = page + 1), previousPageUrl = flask.url_for('page', page = page - 1))

@app.route('/rss.xml')
def rss():
    posts = Post.posts_by_page(posts_per_page = 20)
    response = flask.make_response(flask.render_template('rss.xml', posts = posts), 200)
    response.headers['content-type'] = "application/rss+xml"
    return response

@app.route('/about.html')
def about():
    return flask.render_template('about.html')

@app.route('/page<int:page>')
def page(page):
    if page < 2:
        return flask.redirect(flask.url_for('index'), 301)
    else:
      total_pages = Post.total_pages()
      if page > total_pages:
        return flask.redirect(flask.url_for('index'), 301)
      else:
        posts = Post.posts_by_page(page)
        return flask.render_template('index.html', posts = posts, page = page, total_pages = total_pages, nextPageUrl = flask.url_for('page', page = page + 1), previousPageUrl = flask.url_for('page', page = page - 1))

@app.route('/<slug>.html', methods=['GET'])
def read(slug):
    post = Post.objects(slug = slug)[0]
    return flask.render_template('post.html', post = post)

@app.route('/post')
def postNew():
    today = datetime.datetime.today()
    return flask.render_template('post/new.html', today = today)

@app.route('/post', methods=['POST'])
def postSave():
    app.open_session(flask.request)
    post = Post()
    post.init_from_dict(flask.request.form)
    import re
    post.body = re.sub(r'(<!--.*?-->|<[^>]*>)', '', post.body)
    post.ip = flask.request.remote_addr
    try:
        post.save()
        return flask.redirect(flask.url_for('read', slug = post.slug))
    except (mongoengine.ValidationError) as validationError:
        flask.flash(validationError, category = "error")
        return flask.render_template('post/new.html', post = post, messages = flask.get_flashed_messages(with_categories = True))
    except (mongoengine.OperationError) as operationError:
        flask.flash("A post with this title already exists.", category = "error")
        return flask.render_template('post/new.html', post = post, messages = flask.get_flashed_messages(with_categories = True))
    except Exception as uh_oh:
        flask.flash("Uh oh. An unexpected error has occurred. {}".format(uh_oh), category = "error")
        logging.error(uh_oh)
        return flask.render_template('post/new.html', post = post, messages = flask.get_flashed_messages(with_categories = True))

########## Common Application Functionality
#errors
@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template('error/404notFound.html'), 404

@app.errorhandler(500)
def server_error(error):
    return flask.render_template('error/404notFound.html'), 404

#request
@app.before_request
def before_request():
    """Setup some common daos so we can use them across the board"""
    flask.g.connect = mongoengine.connect('blogizzle')
    flask.g.now = datetime.datetime.now()

@app.after_request
def after_request(response):
    """Destroy"""
    del(flask.g.connect)
    del(flask.g.now)
    return response

########## Custom Jinja2 Filters
def datetimeformat(value, format='%A, %B %d %I:%M %p %Z'):
    return value.strftime(format)

def markdown2html(value):
    return jinja2.Markup(markdown.markdown(value))

def gravatar(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (hashlib.md5(email.strip().lower().encode('utf-8')).hexdigest(), size)

app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['markdown2html'] = markdown2html
app.jinja_env.filters['gravatar'] = gravatar


########## Debug app - local development server
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)
    app.debug = True
    app.run()
