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
    data = get_static_json("static/projects/projects.json")['projects']
    data.sort(key=order_projects_by_weight, reverse=True)

    tag = request.args.get('tags')
    if tag is not None:
        data = [project for project in data if tag.lower() in [project_tag.lower() for project_tag in project['tags']]]

    return render_template('portfolio.html', projects=data, tag=tag, title="portfolio page")

@app.route('/portfolio/<title>')
def project(title):
    projects = get_static_json("static/projects/projects.json")['projects']

    in_project = next((p for p in projects if p['link'] == title), None)

    if in_project is None:
        return render_template('404.html'), 404
    else:
        selected = in_project

    # load html if the json file doesn't contain a description
    if 'description' not in selected:
        path = "projects"
        selected['description'] = io.open(get_static_file(
            'static/%s/%s/%s.html' % (path, selected['link'], selected['link'])), "r", encoding="utf-8").read()
    return render_template('project.html', project=selected)



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

def order_projects_by_weight(projects):
    try:
        return int(projects['weight'])
    except KeyError:
        return 0

# Error cases
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#TODO FileNotFoundErrors

if __name__ == "__main__":
    app.run(debug=True)