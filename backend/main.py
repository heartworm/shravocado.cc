from flask import Flask, render_template

app = Flask(__name__)



@app.route('/cv')
def cv():
    return render_template('pages/cv.html')

@app.route('/about')
def about():
    return render_template('pages/about.html')

@app.route('/links')
def links():
    return render_template('pages/links.html')


@app.route('/')
def index():
    return render_template('pages/index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)