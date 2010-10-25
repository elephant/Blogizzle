import logging
from flask import Flask, render_template, request

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html', message="hello there")

@app.route('/post/new')
def postNew():
    return render_template('post/new.html')

@app.route('/post/save', methods=['POST'])
def postSave():
    formVals = request.form
    return render_template('post/save.html', formVals = formVals)

#errors
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404notFound.html')

if __name__ == '__main__':
    app.run()