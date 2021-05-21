import io
import json
import os
from flask import Flask, render_template, request, redirect, Response, send_file, abort

app = Flask(__name__)

#Professional side of the page
@app.route("/")
def homepage():
    return render_template("home.html", title="HOME PAGE")

@app.route("/about")
def about():
    return render_template("about.html", title="about page")

@app.route("/portfolio")
def portfolio():
    return render_template("home.html", title="portfolio page")

@app.route("/research")
def research():
    return render_template("home.html", title="research page")

# Personal Side of the page
@app.route("/personal")
def personal():
    return render_template("personalhome.html", title="personal page")

@app.route("/personal/blog")
def blog():
    return render_template("personalhome.html", title="blog page")

@app.route("/personal/art")
def art():
    return render_template("personalhome.html", title="art page")

@app.route("/personal/food")
def food():
    return render_template("personalhome.html", title="food page")

@app.route("/personal/misc")
def misc():
    return render_template("personalhome.html", title="misc page")


# Helper functions
def get_static_file(path):
    site_root = os.path.realpath(os.path.dirname(__file__))
    return os.path.join(site_root, path)

def get_static_json(path):
    return json.load(open(get_static_file(path)))

# Error cases
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)