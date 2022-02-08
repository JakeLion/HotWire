from flask import Flask, render_template
import socket



ip = input("Server IP:")
port1 = input("Server port:")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def er_500(e):
    return render_template("500.html")

@app.errorhandler(403)
def er_403(e):
    return render_template("403.html")

@app.errorhandler(410)
def er_410(e):
    return render_template("410.html")

if __name__ == "__main__":
    app.run(host=ip, port=port1)
