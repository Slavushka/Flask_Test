from flask import Flask, render_template, url_for, request, session, redirect

app = Flask(__name__)


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if "userlogged" in session:
        return redirect(url_for("profile", username=session["userlogged"]))
    elif (
        request.method == "POST"
        and request.form["username"] == "slavushka"
        and request.form["psw"] == "123456"
    ):
        session["userlogged"] = request.form["username"]
        return redirect(url_for("profile", username=session["userlogged"]))
    return render_template("login.html")


@app.errorhandler(404)
def pageNotFound(error):
    # return render_template("page404.html")  # код 200
    return render_template("page404.html"), 404  # код 404


if __name__ == "__main__":
    app.run(debug=True)
