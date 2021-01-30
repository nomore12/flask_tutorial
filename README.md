# 설치

```cmd
> git clone https://github.com/nomore12/flask_tutorial.git
> cd flask_tutorial
> python3 -m venv venv
```

## 실행

```cmd
> venv\Scripts\activate
> pip3 install -r requirements.txt
> cd project
> python3 app.py
```

# 데이터베이스 셋업

```cmd
> cd project
> python3 create_database.py
```

## 유저 생성

linux 환경이라 윈도우에선 어떨지 모르겠음.

```cmd
> sqlite3 database.db
> .mod column
> INSERT INTO user (username, email, datetime) values ('name', 'nomore@naver.com', '2021-01-30')
> .quit
```
