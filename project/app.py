from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST', 'GET'])
def result(name=None):
    if request.method != "POST":
        return redirect('/')
    food = request.form['food']
    if food != '김치':
        return redirect('/')
    result = {'food': food, "food2": "dsdfasdfag"}
    return render_template('result.html', **{"food": food, "food2": "복숭아"})


lst = [ { "name": "노성호", "birth": "07/18" }, { "name": "강지능", "birth": "12/10" },{ "name": "임한국", "birth": "04/43" },{ "name": "이선주", "birth": "09/10" } ]

@app.route('/list')
def list():
    return render_template('list.html', lst=lst)

@app.route('/person/<int:id>')
def person(id):
    return render_template(
        'detail.html', 
        name=lst[id-1]['name'],
        birth=lst[id-1]['birth']
        )


if __name__ == '__main__':
    app.debug = True
    app.run()
