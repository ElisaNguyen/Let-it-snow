from flask import Flask, render_template
import animation


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/', methods=["POST"])
def let_it_snow():
    animation.let_it_snow()
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
