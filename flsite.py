from flask import Flask, url_for

app = Flask(__name__)


@app.route("/")
@app.route("/index")  # url_for возвращает ближайший к функции url-адрес
def index():
    print(url_for("index"))
    return "Главная страница"


@app.route("/profile1/<username>")  # /profile1/slavushka
def profile1(username):
    print(username)
    return "Страница пользователя - 1"


@app.route("/profile2/<path:username>")  # /profile2/slavushka/page1
def profile2(username):
    print(username)
    return "Страница пользователя -2"


@app.route("/profile3/<int:username>")  # /profile3/123456
def profile3(username):
    print(username)
    return "Страница пользователя - 3"


# Запуск сервера
# if __name__ == "__main__":
#     app.run(debug=True)

# Искусственный контекст запроса без запуска сервера
with app.test_request_context():
    print(url_for("index"))
    print(url_for("profile1", username="slavushka"))
    print(url_for("profile2", username="slavushka/page1"))
    print(url_for("profile3", username="123456"))
