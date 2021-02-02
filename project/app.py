from pathlib import Path
from datetime import datetime
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, session, current_app

from query import get_all_articles, get_all_users, get_user, get_article, create_article, create_user, get_user_by_email
from configs import dictConfig


app = Flask(__name__)

dictConfig


@app.template_filter('today')
def format_datetime(value):
    return value[11:16]


@app.route('/404')
def http_404():
    return render_template('http_404.html')


@app.route('/')
def index():
    current_app.logger.debug(session.get('user', 'no user'))
    articles = get_all_articles()
    if session.get("user", "") == "":
        user = None
    else:
        try:
            user = session.get("user", '')
        except Exception as e:
            return redirect(url_for('.http_404', context={'message': e}))
    context = {
        'user': user,
        'articles': articles,
        'users': get_all_users(),
    }
    return render_template('list.html', context=context)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method != 'POST':
        return render_template('login.html')
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    user = get_user_by_email(email)
    current_app.logger.debug(user, email, password)
    if email != user.get('email', '') or password != user.get('password', ''):
        print(email, password)
        return render_template('login.html', context={'message': '이메일이나 패스워드를 다시 확인해 주세요.'})
    session['user'] = user
    return redirect(url_for('.index', context={"user": user}))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method != 'POST':
        return render_template('register.html')
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    password2 = request.form.get('password-confirm', '').strip()
    if username == '' or email == '' or password == '' or password2 == '':
        return render_template('register.html')
    if password != password2:
        return render_template('register.html')
    create_user(username, email, password)
    return redirect(url_for('.index'))


# 유저는 무조건 1번. 하드코딩.
@ app.route('/edit')
def write_article_page():
    return render_template('edit.html', context=get_user(1))


# 1번 유저만 글 쓸 수 있음.
@ app.route('/create', methods=['POST', ])
def write_article():
    if request.method != 'POST':
        return redirect(url_for('.create'))
    user_id = request.form['user_id']
    title = request.form['title']
    content = request.form['content']
    create_article(user_id, title, content)

    return redirect(url_for('.index'))


if __name__ == '__main__':
    app.config.update(
        DEBUG=True,
        SECRET_KEY='secretkey',
    )
    app.run()
