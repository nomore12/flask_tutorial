from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def execute_query(query):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    sql = cursor.execute(query).fetchall()
    conn.close()
    print(sql)
    return sql

@app.route('/')
def index():
    query = "select * from user;"
    context = execute_query(query)
    return render_template('base.html', context=context[0])


if __name__ == '__main__':
    app.debug = True
    app.run()
