from pathlib import Path
from datetime import datetime
import sqlite3
from pprint import pprint
import json
from datetime import timedelta

from flask import Flask, render_template, request, redirect, url_for, session, current_app

from query import get_all_articles, get_all_users, get_user, get_article, create_article, create_user, get_user_by_email
from configs import dictConfig


app = Flask(__name__)


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


@app.template_filter('today')
def format_datetime(value):
    return value[11:16]


@app.route('/404')
def http_404():
    return render_template('http_404.html')


@app.route('/')
def index():
    current_app.logger.debug(str(session.get('user', '없음')))
    current_app.logger.debug(f"list session: {str(session)}")
    articles = get_all_articles()
    user = session.get('user', '')
    context = {
        'user': user,
        'articles': articles,
    }
    return render_template('list.html', context=context)


@app.route('/article/<id>')
def article_detail(id):
    current_app.logger.debug(f"edit session: {str(session)}")
    article = get_article(id)
    article['content'] = article['content'].replace('\n', '<br>')
    user = session.get('user', '')
    if user == '':
        current_app.logger.debug('로그인 되어있는 유저가 없습니다.')
        return redirect(url_for('.login'))
    return render_template('detail.html', context={'article': article})


@app.route('/login', methods=['POST', 'GET'])
def login():
    current_app.logger.debug(f"login session: {str(session)}")
    if request.method != 'POST':
        return render_template('login.html', context={'message': None})
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    user = get_user_by_email(email)
    if (user is None) or email != user.get('email', '') or password != user.get('password', ''):
        return render_template('login.html', context={"message": "로그인 이메일이나 패스워드를 다시 확인해주세요."})
    session['user'] = user
    current_app.logger.debug(f"로그인 한 유저의 이름은 {user.get('username', '')}입니다.")
    # 로그인 성공 화면으로 바꿔야 함.
    return redirect(url_for('.index'))


@app.route('/logout')
def logout():
    current_app.logger.debug(f"logout session: {str(session)}")
    if session.get('user', '') == '':
        return redirect(url_for(('.index'), context={'user': None}))
    session.pop('user')
    current_app.logger.debug(str(session.get('user', '로그인 된 유저가 없습니다.')))
    # 로그아웃 성공 화면으로 바꿔야 함
    return redirect(url_for(('.index')))


@ app.route('/register', methods=['POST', 'GET'])
def register():
    current_app.logger.debug(f"register session: {str(session)}")
    if request.method != 'POST':
        return render_template('register.html', context={"message": None})
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    password2 = request.form.get('password-confirm', '').strip()
    if username == '' or email == '' or password == '' or password2 == '':
        return render_template('register.html', context={"message": "아이디, 이메일, 패스워드는 모두 입력되어야 합니다."})
    if password != password2:
        return render_template('register.html', context={"message": "패스워드는 동일하게 입력해야 합니다."})
    create_user(username, email, password)
    return redirect(url_for('.index'))


@ app.route('/edit/<id>')
def write_article_page(id):
    current_app.logger.debug(f"edit session: {str(session)}")

    if session.get('user', '') == '':
        return redirect(url_for('.login'))
    user = session.get('user', '')

    return render_template('edit.html', context={'user': user})


@app.route('/create', methods=['POST', ])
def write_article():
    current_app.logger.debug(f"create session: {str(session)}")
    if request.method != 'POST':
        return redirect(url_for('.write_article'))
    id = request.form.get('user_id', '')
    title = request.form.get('title', '').strip()
    content = request.form.get('content')
    create_article(id, title, content)
    return redirect(url_for('.index'))


if __name__ == '__main__':
    app.config.update(
        DEBUG=True,
        SECRET_KEY='secretkey',
    )
    app.run()
