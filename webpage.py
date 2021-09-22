"""
Test-environment main class
"""
from flask import Flask, request, redirect, url_for, render_template, session
from datetime import timedelta
from user_recognition import UserRecognition
from data import Data
from content import PageContent

app = Flask(__name__)
app.secret_key = "afjhak&$f//DTuhdu)=dB"
app.permanent_session_lifetime = timedelta(minutes=25)


def user_recognition(request, parameter):
    """
    Method for seeing if a user is already identified and otherwise
    calling the user recognition to try to identify the user
    """
    if "user" not in session:
        session.permanent = True
        session["user"] = str(UserRecognition().recognize(request, parameter))
    print(f'Current User: {session["user"]}')
    print(f'user target group: {Data().get_target_group(session["user"])}')


@app.route("/")
def home():
    """
    A Homepage for the website witch explanations and redirects to the webpages
    (redirects will not contain parameters)

    :return: rendering of the file home.html which contains
             all information about this website
    """
    user_recognition(request, parameter=None)
    Data().create_session_entry(request, int(session["user"]), "home.html")
    # there is no Home page implemented yet, therefore it automatically redirects to the ecommerce page
    return redirect(url_for("ecommerce"))
    #return render_template("home.html", base="base.html", bg_color="light", text_color="black")



@app.route("/ecommerce", defaults={'parameter': None})
@app.route("/ecommerce/<parameter>")
def ecommerce(parameter):
    user_recognition(request, parameter)
    response = PageContent().generate_content(parameter, user=session["user"],
                                              request=request, wtype="e-commerce")
    return response


@app.route("/search-engine", defaults={'parameter': None})
@app.route("/search-engine/<parameter>")
def search_engine(parameter):
    template = "search_engine.html"
    user_recognition(request, parameter)
    content = parameter
    return render_template(template, content=content)


@app.route("/news-page", defaults={'parameter': None})
@app.route("/news-page/<parameter>")
def news_page(parameter):
    template = "news_page.html"
    user_recognition(request, parameter)
    content = parameter
    return render_template(template, content=content)


@app.route("/user")
def user():
    usr = session["user"]
    return f"<h1>{usr}</h1>"


if __name__ == "__main__":
    app.run(debug=True)
