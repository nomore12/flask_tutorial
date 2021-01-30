from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from query import get_all_articles, get_all_users, get_user, get_article

app = Flask(__name__)


@app.template_filter('today')
def format_datetime(value):
    return value[11:16]


@app.route('/')
def index():
    articles = get_all_articles()
    user = get_user(1)
    context = {
        'user': user,
        'articles': articles,
    }
    return render_template('list.html', context=context)


@app.route('/write')
def create_article():
    if request.method != 'POST':
        return redirect('/write')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    pass


if __name__ == '__main__':
    app.debug = True
    app.run()
