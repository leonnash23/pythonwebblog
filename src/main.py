from bottle import route, static_file, run, template
from src.database import DataBase


@route("/")
def index():
    posts = DataBase().getAll()
    return template("./src/static/index.html", posts=posts)


@route("/post/<post_id>")
def getPost(post_id):
    post = DataBase().getById(post_id)[0]
    return template("./src/static/post.html", title=post[1], text=post[2], image=post[3])


@route("/<folder>/<file>")
def css(folder, file):
    return static_file(file, root="./src/{0}".format(folder))


@route("/fonts/roboto/<file>")
def css(file):
    return static_file(file, root="./src/{0}/{1}".format("fonts", "roboto"))


run(host="localhost", port=8080)
