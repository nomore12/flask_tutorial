import sqlite3
from datetime import datetime


'''
    cursor란...
    A database cursor is an identifier associated with a group of rows. It is, in a sense, a pointer to the current row in a buffer.

    You must use a cursor in the following cases:
    - Statements that return more than one row of data from the database server:
        - A SELECT statement requires a select cursor.
        - An EXECUTE FUNCTION statement requires a function cursor.
    - An INSERT statement that sends more than one row of data to the database server requires an insert cursor.
'''


def get_all_users():
    # 그냥 다 가져옴
    sql = "SELECT * FROM user ORDER BY id DESC;"
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    users = c.execute(sql).fetchall()
    conn.close()
    return users


def get_user(id):
    sql = f"SELECT * FROM user WHERE id = '{id}';"
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    user = cursor.execute(sql).fetchone()
    conn.close()
    return user


# 개어려움
def get_all_articles():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    # sql = 'SELECT * FROM article;'
    sql = "SELECT atc.id, usr.username, atc.title, atc.created_at FROM article atc LEFT OUTER JOIN user usr ON atc.user_id = usr.id;"

    cursor = conn.cursor()
    cursor.execute(sql)
    content = cursor.fetchall()

    result = []
    for row in content:
        data = {}
        # list loop에서 인덱스도 함께 쓰고 싶을때 index, value 형태로 쓰면 됨.
        for index, key in enumerate(row.keys()):
            data[key] = tuple(row)[index]
        result.append(data)

    result = sorted(
        result, key=lambda e: e['id'], reverse=True
    )
    conn.close()
    return result


def get_article(id):
    sql = f"SELECT id, title, content, created_at, (SELECT id FROM user WHERE user_id = id) as user_id FROM article WHERE id = '{id}';"

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    article = cursor.execute(sql).fetchone()
    conn.close()
    return article


def create_user(username, email):
    # 현재 시간을 문자열로 변환. "2021-01-30 12:53:37" 형태로 변환
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # f String의 {}안에 변수를 넣는 형태로 간단하게 쿼리문 작성. VALUES의 인자값에는 문자열이 들어간다고 방심하기 말고 {}밖에 따옴표를 꼭 넣어야 함...
    sql = f"INSERT INTO user (username, email, created_at) \
        VALUES ('{username}', '{email}', '{now}'); "

    # 데이터베이스에 접속
    conn = sqlite3.connect('database.db')

    # 데이터베이스의 커서를 생성. 커서에 sql문을 삽입 후 데이터베이스 커넥션에서 커서의 sql문을 커밋(실행)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    # 데이터베이스를 닫는다.
    conn.close()


# create_user와 동일
def create_article(user_id, title, content):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = f"INSERT INTO article (user_id, title, content, created_at) VALUES ((SELECT id FROM user WHERE id={user_id}), '{title}', '{content}', '{now}'); "
    print(sql)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


# get_all_articles()
# articles = get_all_articles()
# article_dict = [{
#     'created_at': item[3],
#     'id': item[0],
#     'username': item[1],
#     'title': item[2],
# } for item in articles]
# print(type(article_dict))

# for item in article_dict:
#     print(type(item))
#     print(item)
