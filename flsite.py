from flask import Flask, render_template, request

app = Flask(__name__)

# menu = ["Установка", "Первое приложение", "Обратная связь"]
menu = [
    {"name": "Установка", "url": "install-flask"},
    {"name": "Первое приложение", "url": "first-app"},
    {"name": "Обратная связь", "url": "contact"},
]


@app.route("/")
def index():
    return render_template("index.html", title="Главная страница", menu=menu)


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        print(request.form)
        print("Имя пользователя:", request.form["username"])
    return render_template("contact.html", title="Обратная связь", menu=menu)


if __name__ == "__main__":
    app.run(debug=True)
