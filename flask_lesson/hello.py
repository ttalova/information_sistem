# необходимые импорты
import json
from flask import Flask, render_template, request

# инициализируем приложение
# из документации:
#     The flask object implements a WSGI application and acts as the central
#     object.  It is passed the name of the module or package of the
#     application.  Once it is created it will act as a central registry for
#     the view functions, the URL rules, template configuration and much more.
app = Flask(__name__)

# дальше реализуем методы, которые мы можем выполнить из браузера,
# благодаря указанным относительным путям


# метод, который возвращает список фильмов по относительному адресу /films
@app.route("/films", methods=['GET', 'POST'])
def films_list():
    if request.method == 'POST':
        with open('films.json', 'r') as f:
            data = json.load(f)
        data.append(request.form)

        with open('films.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=True)

    # читаем файл с фильмами
    with open("films.json", 'r') as f:
        films = json.load(f)
        # получаем GET-параметр country (Russia/USA/French
    country = request.args.get("country")
    rating = request.args.get("rating")
    if rating:
        films = [x for x in films if float(x['rating']) >= float(rating)]
    # формируем контекст, который мы будем передавать для генерации шаблона
    context = {
        'films': films,
        'title': "FILMS",
        'country': country
    }
    # возвращаем сгенерированный шаблон с нужным нам контекстом
    return render_template("films.html", **context)

# метод, который возвращает конкретный фильмо по id по относительному пути /film/<int:film_id>,
# где film_id - id необходимого фильма
@app.route("/film/<int:film_id>")
def get_film(film_id):
    # читаем файл
    with open("films.json", 'r') as f:
        films = json.load(f)

    # ищем нужный нам фильм и возвращаем шаблон с контекстом
    for film in films:
        if int(film['id']) == int(film_id):
            return render_template("film.html", title=film['name'], film=film)

    # если нужный фильм не найден, возвращаем шаблон с ошибкой
    return render_template("error.html", error="Такого фильма не существует в системе")

# @app.route("/films/<int:rating_id>", methods=['GET', 'POST'])
# def get_film_list(rating_id):
#     with open("films.json", 'r') as f:
#         films = json.load(f)
#         films = [x for x in films if x['rating'] >= rating_id]
#         rating = request.args.get("rating")
#         context = {
#             'films': films,
#             'title': "FILMS",
#             'rating': rating
#         }
#     return render_template("films.html", **context)

