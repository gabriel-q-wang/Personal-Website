import io
import json
import os
from flask import Flask, render_template, request, redirect, Response, send_file, abort

app = Flask(__name__)

#########################################################
# Helper functions
#########################################################
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

def get_common_links():
    return get_static_json("static/commonlinks.json")

#########################################################
#Professional side of the page
#########################################################
@app.route("/")
def homepage():
    return render_template("professional/home.html", title="HOME PAGE", commonlinks=get_common_links())

@app.route("/about")
def about():
    return render_template("professional/about.html", title="about page", commonlinks=get_common_links())

@app.route("/portfolio")
def portfolio():
    data = get_static_json("static/projects/projects.json")['projects']
    data.sort(key=order_projects_by_weight)
    data = [proj for proj in data if proj['weight'] >= 0]

    tag = request.args.get('tags')
    if tag is not None:
        data = [project for project in data if tag.lower() in [project_tag.lower() for project_tag in project['tags']]]

    return render_template('professional/portfolio.html', projects=data, tag=tag, title="portfolio page", commonlinks=get_common_links(), section='portfolio')

@app.route('/portfolio/<title>')
def project(title):
    projects = get_static_json("static/projects/projects.json")['projects']

    in_project = next((p for p in projects if p['link'] == title), None)

    if in_project is None:
        return render_template('common/404.html'), 404
    else:
        selected = in_project

    # load html if the json file doesn't contain a description
    if 'description' not in selected:
        path = "projects"
        selected['description'] = io.open(get_static_file(
            'static/%s/%s/%s.html' % (path, selected['link'], selected['link'])), "r", encoding="utf-8").read()
    return render_template('common/project.html', base='professional/base.html', project=selected, path='portfolio', commonlinks=get_common_links())



@app.route("/research")
def research():
    return render_template("professional/research/home.html", title="research page", commonlinks=get_common_links())

@app.route("/research/labs")
def labs():
    return render_template("professional/research/labs.html", title="research labs", commonlinks=get_common_links())

@app.route("/research/papers")
def papers():
    return render_template("professional/research/papers.html", title="research papers", commonlinks=get_common_links())

@app.route("/research/summaries")
def summaries():
    return render_template("professional/research/summaries.html", title="research summaries", commonlinks=get_common_links())

#########################################################
# Personal Side of the page
#########################################################
@app.route("/personal")
def personal():
    return render_template("personal/home.html", title="personal page", commonlinks=get_common_links())

@app.route("/personal/blog")
def blog():
    data = get_static_json("static/blog/blog.json")['blog']
    data.sort(key=order_projects_by_weight)
    data = [proj for proj in data if proj['weight'] >= 0]

    tag = request.args.get('tags')
    if tag is not None:
        data = [project for project in data if tag.lower() in [project_tag.lower() for project_tag in project['tags']]]

    return render_template("personal/blog.html", title="blog page", projects=data, tag=tag, section='personal/blog')

@app.route('/personal/blog/<title>')
def blog_post(title):
    projects = get_static_json("static/blog/blog.json")['blog']

    in_project = next((p for p in projects if p['link'] == title), None)

    if in_project is None:
        return render_template('common/404.html'), 404
    else:
        selected = in_project

    # load html if the json file doesn't contain a description
    if 'description' not in selected:
        path = "blog"
        selected['description'] = io.open(get_static_file(
            'static/%s/%s/%s.html' % (path, selected['link'], selected['link'])), "r", encoding="utf-8").read()
    return render_template('common/project.html', base='personal/base.html', project=selected, path='blog')

@app.route("/personal/art")
def art():
    data = get_static_json("static/art/art.json")['art']
    data.sort(key=order_projects_by_weight)
    data = [proj for proj in data if proj['weight'] >= 0]

    tag = request.args.get('tags')
    if tag is not None:
        data = [project for project in data if tag.lower() in [project_tag.lower() for project_tag in project['tags']]]

    return render_template("personal/art.html", title="art page", projects=data, tag=tag, section='personal/art')

@app.route('/personal/art/<title>')
def art_post(title):
    projects = get_static_json("static/art/art.json")['art']

    in_project = next((p for p in projects if p['link'] == title), None)

    if in_project is None:
        return render_template('common/404.html'), 404
    else:
        selected = in_project

    # load html if the json file doesn't contain a description
    if 'description' not in selected:
        path = "art"
        selected['description'] = io.open(get_static_file(
            'static/%s/%s/%s.html' % (path, selected['link'], selected['link'])), "r", encoding="utf-8").read()
    return render_template('common/project.html', base='personal/base.html', project=selected, path='art')

@app.route("/personal/food")
def food():
    data = get_static_json("static/food/food.json")['food']
    data.sort(key=order_projects_by_weight)
    data = [proj for proj in data if proj['weight'] >= 0]

    tag = request.args.get('tags')
    if tag is not None:
        data = [project for project in data if tag.lower() in [project_tag.lower() for project_tag in project['tags']]]

    return render_template("personal/food.html", title="food page", projects=data, tag=tag, section='personal/food')

@app.route('/personal/food/<title>')
def food_post(title):
    projects = get_static_json("static/food/food.json")['food']

    in_project = next((p for p in projects if p['link'] == title), None)

    if in_project is None:
        return render_template('common/404.html'), 404
    else:
        selected = in_project

    # load html if the json file doesn't contain a description
    if 'description' not in selected:
        path = "food"
        selected['description'] = io.open(get_static_file(
            'static/%s/%s/%s.html' % (path, selected['link'], selected['link'])), "r", encoding="utf-8").read()
    return render_template('common/project.html', base='personal/base.html', project=selected, path='food')

@app.route("/personal/misc")
def misc():
    data = get_static_json("static/misc/misc.json")['misc']
    data.sort(key=order_projects_by_weight)
    data = [proj for proj in data if proj['weight'] >= 0]

    tag = request.args.get('tags')
    if tag is not None:
        data = [project for project in data if tag.lower() in [project_tag.lower() for project_tag in project['tags']]]

    return render_template("personal/misc.html", title="misc page", projects=data, tag=tag, section='personal/misc')

@app.route('/personal/misc/<title>')
def misc_post(title):
    projects = get_static_json("static/misc/misc.json")['misc']

    in_project = next((p for p in projects if p['link'] == title), None)

    if in_project is None:
        return render_template('common/404.html'), 404
    else:
        selected = in_project

    # load html if the json file doesn't contain a description
    if 'description' not in selected:
        path = "misc"
        selected['description'] = io.open(get_static_file(
            'static/%s/%s/%s.html' % (path, selected['link'], selected['link'])), "r", encoding="utf-8").read()
    return render_template('common/project.html', base='personal/base.html', project=selected, path='misc')


#########################################################
# Error cases
#########################################################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('common/404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)