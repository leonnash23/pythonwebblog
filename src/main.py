import os

from bottle import route, static_file, run, template, post, request
from database import DataBase


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


@route("/createPost")
def cretepost():
    return static_file("createPost.html", root="./src/static")


@post("/confirmPost")
def do_login():
    title = request.forms.get("title")
    text = request.forms.get("text")
    f = request.files.get("file")
    db = DataBase()
    name, ext = os.path.splitext(f.filename)
    try:
        post_id = str(int(db.getAll()[-1][0]) + 1)
    except:
        post_id = str(1)
    file_name = post_id + ext
    file_path = "{path}/{file}".format(path="./src/images", file=file_name)
    with open(file_path, 'wb') as open_file:
        open_file.write(f.file.read())
    db.addNew(title, text, file_name)
    return """<p>Post created</p><a href="../post/{0}">Пост</a>""".format(post_id)


@route("/getArchive")
def getArchive():
    import zipfile
    zipf = zipfile.ZipFile('Archive.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk("."):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()
    return static_file("Archive.zip", root='.', download="Archive.zip")


run(host="localhost", port=8080)
# run(host="0.0.0.0", port=os.environ['PORT'])
