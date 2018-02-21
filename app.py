# to run:
# FLASK_APP=app.py flask run

from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello world!"

if __name__ == "__main__":
    app.run()
