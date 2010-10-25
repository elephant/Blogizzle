from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post/new')
def postNew():
    return render_template('post/new.html')

@app.route('/post/save', methods=['POST'])
def postSave():
    return render_template('post/save.html')

#errors
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404notFound.html')

if __name__ == '__main__':
    app.run()