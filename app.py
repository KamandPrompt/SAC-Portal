from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/name/<name>")
def getName(name):
    return "name : {}".format(name)

if __name__ == '__main__':
    app.run()