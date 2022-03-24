from flask import Flask, render_template, url_for
from scraper import data


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
