from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from query import get_all_articles, get_all_users, get_user, get_article, create_article
from datetime import datetime


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


# 유저는 무조건 1번. 하드코딩.
@app.route('/edit')
def write_article_page():
    return render_template('edit.html', context=get_user(1))


# 1번 유저만 글 쓸 수 있음.
@app.route('/create', methods=['POST', ])
def write_article():
    if request.method != 'POST':
        return redirect(url_for('.create'))
    user_id = request.form['user_id']
    title = request.form['title']
    content = request.form['content']
    create_article(user_id, title, content)
    return redirect(url_for('.index'))


if __name__ == '__main__':
    app.debug = True
    app.run()
