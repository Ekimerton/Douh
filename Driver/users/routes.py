import os
from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from Driver import db, bcrypt
from Driver.models import User, Recipe, Ingredient
from Driver.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from Driver.posts.forms import IngredientForm
from Driver.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

# Summary: The registeration page for new users. Calls the RegistrationForm, hashes the password before storing.
# TODO: Possibly do a redesign.
@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)

# Summary: Asks for the user's email and password, sees if they are in the system.
# TODO: Possible redesign, along with the registeration.
@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        flash(f"Login unsuccessful. Please check your email and password!", "danger")
    return render_template("login.html", title="Login", form=form)

# Summary: Logout page, no html is rendered, just logs the user out and redirects them home.
# TODO: Nothing.
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


# Summary: Shows the current user's information, and allows them to change it. When the picture is changed, and the old picture wasn't the default, the old picture is deleted.
# TODO: Nothing.
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("users.account"))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form)

# Summary: Does the same thing as the home route, but only shows the recipes for the requested user in the params.
# TODO: Nothing.
@users.route("/user/<string:username>")
def user_recipes(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Recipe.query.filter_by(author=user)\
    .order_by(Recipe.date.desc())\
    .paginate(page=page, per_page=5)
    return render_template("user_posts.html", posts=posts, user=user)

# Summary: A 1-2-combo. Shows a form to add ingredients at the top, and shows the user's ingredients at the bottom, paginated 5 at a time.
# TODO: I'd like to add interchangability between units.
    #e.g: tablespoons to cups to millilitres
@users.route("/ingredients/<string:username>", methods=['GET', 'POST'])
@login_required
def user_ingredients(username):
    form = IngredientForm()
    if form.validate_on_submit():
        pricePer = (form.price.data / form.amount.data)
        post = Ingredient(name=form.name.data, price=pricePer, unit=form.unit.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your Ingredient has been created!", "success")
        return redirect(url_for('users.user_ingredients', username=current_user.username))
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Ingredient.query.filter_by(author=user)\
    .order_by(Ingredient.name.desc())\
    .paginate(page=page, per_page=5)
    return render_template("ingredients.html", posts=posts, user=user, form=form)

# Summary: Same as the delete post route, but instead searches for the entry within the Ingredient database. Redirects to home.
# TODO: Nothing.
@users.route("/ingredient/<int:ingredient_id>/delete", methods=['POST'])
@login_required
def delete_ingredient(ingredient_id):
    post = Ingredient.query.get_or_404(ingredient_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your ingredient has been deleted!", "success")
    return redirect(url_for('users.user_ingredients', username=current_user.username))


# Summary: Page for letting the user enter an email, and then calling the send_reset_email function with that email.
# TODO: Maybe redesign, along with the other login/registeration stuff.
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instuctions to reset your password!", "info")
        return redirect(url_for('users.login'))
    return render_template("reset_request.html", title="Reset Password", form=form)

# Summary: This link is sent with the email, and if the received token isn't expired, then the user enters a new password.
# TODO: Nothing.
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if not user:
        flash("That is an invalid (or expired) token!", "warning")
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pass
        db.session.commit()
        flash(f"Password updated! You may now log in.", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title="Reset Password", form=form)
