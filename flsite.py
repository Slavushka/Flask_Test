import sqlite3
import os
from flask import Flask, render_template, g, request, flash, abort
from FDataBase import FDataBase

# Конфигурация
DATABASE = "/tmp/flsite.db"
DEBUG = True
SECRET_KEY = "abrakadabra64423424635634"

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, "flsite.db")))


def connect_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource("sq_db.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()  # Лишняя функция, т.к. with сам закроет после работы с файлом


# Запуск функции создания БД, без запуска сервера, в терминале:
# python
# from flsite import create_db
# create_db()


def get_db():
    """Соединение с БД, если оно ещё не установлено"""
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db


@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template(
        "index.html", menu=dbase.getMenu(), posts=dbase.getPostsAnnonce()
    )


@app.route("/add_post", methods=["POST", "GET"])
def addPost():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        if len(request.form["name"]) > 4 and len(request.form["post"]) > 10:
            res = dbase.addPost(
                request.form["name"], request.form["post"], request.form["url"]
            )
            if not res:
                flash("Ошибка добавления статьи", category="error")
            else:
                flash("Статья добавлена успешно", category="success")
        else:
            flash("Ошибка добавления статьи", category="error")
    return render_template(
        "add_post.html", menu=dbase.getMenu(), title="Добавление статьи"
    )


@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с БД, если оно было установлено"""
    if hasattr(g, "link_db"):
        g.link_db.close()


# @app.route("/post/<int:id_post>")
# def showPost(id_post):
@app.route("/post/<alias>")
def showPost(alias):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)
    return render_template("post.html", menu=dbase.getMenu(), post=post)


if __name__ == "__main__":
    app.run(debug=True)
