from flask import Flask,render_template
from dbHandle import dbHandle

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('pingfen.html')

if __name__ == '__main__':
    app.run()