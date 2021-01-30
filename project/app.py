from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from query import get_all_articles, get_all_users, get_user, get_article

app = Flask(__name__)


@app.template_filter('today')
def format_datetime(value):
    return value[11:16]


def execute_query(query):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    sql = cursor.execute(query).fetchall()
    conn.close()
    print(sql)
    return sql


@app.route('/')
def index():
    articles = get_all_articles()
    return render_template('list.html', context=articles)


@app.route('/list')
def list_view():
    data = get_all_articles()
    return render_template('list.html', context=data)


if __name__ == '__main__':
    app.debug = True
    app.run()
