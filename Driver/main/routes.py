from flask import Blueprint, render_template, request
from Driver.models import Recipe

main = Blueprint('main', __name__)

# Summary: The default page. Shows everyone's posts, sorted by date so the newest posts show first. Paginated so 5 posts show per page.
# TODO: Nothing.
@main.route("/")
@main.route("/about")
def intro():
    return render_template("intro.html")

@main.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Recipe.query.order_by(Recipe.date.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", posts=posts)

# Summary: A static about page.
# TODO: Fill it with actual content.
@main.route("/lol")
def about():
    return render_template('about.html', title='Emptylol')
