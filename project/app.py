from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST', 'GET'])
def result(name=None):
    if request.method != "POST":
        return redirect('/')
    name = request.form['name']
    if name != '김치':
        return redirect('/')
    return render_template('result.html', name=name)


if __name__ == '__main__':
    app.debug = True
    app.run()
