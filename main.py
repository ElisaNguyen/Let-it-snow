from flask import Flask, render_template
import animation


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/', methods=["POST"])
def let_it_snow():
    animation.let_it_snow(2)
    return render_template("home.html")


@app.route('/math_bg')
def math_bg():
    return render_template("math_background.html")


if __name__ == "__main__":
    app.run(debug=True)
