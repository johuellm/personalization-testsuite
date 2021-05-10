"""
Test-environment
"""
from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)


@app.route("/")
def home():
    """
    A Homepage for the website witch explanations and redirects to the webpages
    (redirects will not contain parameters)

    :return: rendering of the file home.html which contains
             all information about this website
    """
    return render_template("home.html")


@app.route("/redirect")
def redirect():
    return redirect(url_for("home"))


@app.route("/ecommerce", defaults={'parameter': None})
@app.route("/ecommerce/<parameter>")
def ecommerce(parameter):
    if parameter is not None:
        content = parameter.split("&")
    else:
        content = []
    content.append("end")
    return render_template("e_commerce.html", content=content)


@app.route("/search-engine", defaults={'parameter': None})
@app.route("/search-engine/<parameter>")
def search_engine(parameter):
    content = parameter
    return render_template("search_engine.html", content=content)


@app.route("/news-page", defaults={'parameter': None})
@app.route("/news-page/<parameter>")
def news_page(parameter):
    content = parameter
    return render_template("news_page.html", content=content)


if __name__ == "__main__":
    app.run(debug=True)
