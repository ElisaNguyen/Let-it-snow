from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/math_bg')
def math_bg():
    return render_template("math_background.html")


if __name__ == "__main__":
    app.run(debug=True)