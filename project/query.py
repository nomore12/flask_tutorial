import sqlite3
from datetime import datetime
from flask import current_app

'''
    cursor란...
    A database cursor is an identifier associated with a group of rows. It is, in a sense, a pointer to the current row in a buffer.

    You must use a cursor in the following cases:
    - Statements that return more than one row of data from the database server:
        - A SELECT statement requires a select cursor.
        - An EXECUTE FUNCTION statement requires a function cursor.
    - An INSERT statement that sends more than one row of data to the database server requires an insert cursor.
'''


# cursor.fetchall() 또는 cursor.fetchone()의 리턴 자료형이 튜플이라 템플릿에서 쓰기 애매함. 딕셔너리로 바꿔주는 함수. 개어려움
def cursor_to_dictionary(query, many=True):
    conn = sqlite3.connect('database.db')
    # https://docs.python.org/ko/3/library/sqlite3.html#row-objects
    # sqlite3.Cursor 객체로 딕셔너리를 만들 수 있음.
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query)
    result = []
    if many:
        content = cursor.fetchall()
        for row in content:
            data = {}
            # list loop에서 인덱스도 함께 쓰고 싶을때 index, value 형태로 쓰면 됨.
            for index, key in enumerate(row.keys()):
                data[key] = tuple(row)[index]
            result.append(data)
    else:
        content = cursor.fetchone()
        result = dict(content)
    conn.close()
    return result


def get_all_users():
    sql = "SELECT * FROM user ORDER BY id DESC;"
    users = cursor_to_dictionary(sql)
    return users


def get_user(id):
    sql = f"SELECT * FROM user WHERE id = '{id}';"
    user = cursor_to_dictionary(sql, False)
    return user


def get_user_by_email(email):
    sql = f"SELECT * FROM user WHERE email = '{email}';"
    user = cursor_to_dictionary(sql, False)
    return user


def get_all_articles():
    # left outer join. article의 user_id를 이용해서 글을 작성한 유저의 정보를 찾음.
    sql = "SELECT atc.id, usr.username, atc.title, atc.created_at FROM article atc LEFT OUTER JOIN user usr ON atc.user_id = usr.id;"
    result = cursor_to_dictionary(sql)
    result = sorted(
        result, key=lambda e: e['id'], reverse=True
    )
    return result


def get_article(id):
    sql = f"SELECT id, title, content, created_at, (SELECT id FROM user WHERE user_id = id) as user_id FROM article WHERE id = '{id}';"
    article = cursor_to_dictionary(sql, False)
    return article


def create_user(username, email, password):
    print(username, email, password)
    # 현재 시간을 문자열로 변환. "2021-01-30 12:53:37" 형태로 변환
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # sql = f"INSERT INTO user (username, email, password, created_at) \
    # VALUES('{username}', '{email}', '{password}', '{now}'); "
    sql = "INSERT INTO user (username, email, password, created_at) \
        VALUES (?, ?, ?, ?);"
    current_app.logger.debug(sql)
    # 데이터베이스에 접속
    conn = sqlite3.connect('database.db')
    # 데이터베이스의 커서를 생성. 커서에 sql문을 삽입 후 데이터베이스 커넥션에서 커서의 sql문을 커밋(실행)
    cursor = conn.cursor()
    # query를 실행한다.
    cursor.execute(sql, (username, email, password, now))
    # 실행한 쿼리를 적용한다.
    conn.commit()
    # 데이터베이스를 닫는다.
    conn.close()


"""
SQLite가 역슬래시 이스케이프를 지원하지 않아서 그렇습니다.
"'작은따옴표"처럼 큰따옴표와 작은따옴표를 그때그때 잘 바꿔 쓰거나, '''escaped' 처럼 ''로 이스케이프하거나, c.execute("UPDATE table SET column = ? WHERE other_column = ?", (100, "'escaped")) 처럼 파라미터화된 쿼리를 쓰세요.
"""


# create_user와 동일
def create_article(user_id, title, content):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = "INSERT INTO article (user_id, title, content, created_at) VALUES ((SELECT id FROM user WHERE id=?), ?, ?, ?);"

    # 데이터베이스에 접속
    conn = sqlite3.connect('database.db')
    # 데이터베이스의 커서를 생성. 커서에 sql문을 삽입 후 데이터베이스 커넥션에서 커서의 sql문을 커밋(실행)
    cursor = conn.cursor()
    # query를 실행한다.
    cursor.execute(sql, (user_id, title, content, now))
    # 실행한 쿼리를 적용한다.
    conn.commit()
    # 데이터베이스를 닫는다.
    conn.close()
