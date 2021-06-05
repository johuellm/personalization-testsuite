"""
Test-environment
Todo:-Empty Session Entry for e_commerce
Todo:-User Target group is None/user not found
Todo:-Additional base layout with sidebar
"""
from flask import Flask, request, redirect, url_for, render_template, session, make_response
from datetime import timedelta, datetime
from user_recognition import UserRecognition
from data import Data
from content import PageContent

app = Flask(__name__)
app.secret_key = "afjhak&$f//DTuhdu)=dB"
app.permanent_session_lifetime = timedelta(minutes=25)


def user_recognition(request):
    if "user" not in session:
        session.permanent = True
        session["user"] = str(UserRecognition().recognize(request))
    print(f'Current User: {session["user"]}')


@app.route("/")
def home():
    """
    A Homepage for the website witch explanations and redirects to the webpages
    (redirects will not contain parameters)

    :return: rendering of the file home.html which contains
             all information about this website
    """
    user_recognition(request)
    Data().create_session_entry(request, int(session["user"]), "home.html")
    return render_template("home.html", base="base.html", bg_color="light", text_color="black")


@app.route("/redirect")
def redirect():
    return redirect(url_for("home"))


@app.route("/ecommerce", defaults={'parameter': None})
@app.route("/ecommerce/<parameter>")
def ecommerce(parameter):
    user_recognition(request)
    response = PageContent().generate_content(parameter, user=session["user"],
                                              request=request, wtype="e-commerce")
    return response


@app.route("/search-engine", defaults={'parameter': None})
@app.route("/search-engine/<parameter>")
def search_engine(parameter):
    template = "search_engine.html"
    user_recognition(request)
    content = parameter
    return render_template("search_engine.html", content=content)


@app.route("/news-page", defaults={'parameter': None})
@app.route("/news-page/<parameter>")
def news_page(parameter):
    template = "news_page.html"
    user_recognition(request)
    content = parameter
    return render_template("news_page.html", content=content)


@app.route("/user")
def user():
    usr = session["user"]
    return f"<h1>{usr}</h1>"


if __name__ == "__main__":
    app.run(debug=True)
