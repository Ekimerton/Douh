import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for, request, abort
from Driver.Forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm, IngredientForm
from Driver.Models import *
from Driver import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

# Summary: The default page. Shows everyone's posts, sorted by date so the newest posts show first. Paginated so 5 posts show per page.
# TODO: Nothing.
@app.route("/")
@app.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Recipe.query.order_by(Recipe.date.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", posts=posts)

# Summary: A static about page.
# TODO: Fill it with actual content.
@app.route("/about")
def about():
    return render_template('about.html', title='About')

# Summary: The registeration page for new users. Calls the RegistrationForm, hashes the password before storing.
# TODO: Possibly do a redesign.
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)

# Summary: Asks for the user's email and password, sees if they are in the system.
# TODO: Possible redesign, along with the registeration.
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("home"))
        flash(f"Login unsuccessful. Please check your email and password!", "danger")
    return render_template("login.html", title="Login", form=form)

# Summary: Logout page, no html is rendered, just logs the user out and redirects them home.
# TODO: Nothing.
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

# Summary: A helper function for saving pictures. Takes in the image file, gives it a random hexadecimal name, and saves it in the static folder.
# TODO: Nothing.
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125 ,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

# Summary: Shows the current user's information, and allows them to change it. When the picture is changed, and the old picture wasn't the default, the old picture is deleted.
# TODO: Nothing.
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            if current_user.image_file != "default.jpg":
                old_picture_path = os.path.join(app.root_path, 'static/profile_pics', current_user.image_file)
                os.remove(old_picture_path)

            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form)

# Route for creating new posts, currently handles 5 ingredients.
# TODO: Honestly, this - and the update_post routes are my worst work in this project. The code looks horrible, could work better, but it gets the work done for now. I'd also like to add markdown support for the text fields. 
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    user = User.query.filter_by(username=current_user.username).first_or_404()
    posts = Ingredient.query.filter_by(author=user)\
    .order_by(Ingredient.name.desc())
    ingredient_list = []
    ingredient_list.append(("None", ""))
    for post in posts:
        ing_id = post.name
        ing_name = post.name + " ("  + post.unit + ")"
        ing_info = (ing_id, ing_name)
        ingredient_list.append(ing_info)
    # Setting ingredient field choises to the user's ingredients
    form.ingredient1.choices = ingredient_list
    form.ingredient2.choices = ingredient_list
    form.ingredient3.choices = ingredient_list
    form.ingredient4.choices = ingredient_list
    form.ingredient5.choices = ingredient_list

    if form.validate_on_submit():
        ingredients_raw = str(form.ingredient1_quantity.data) + ":" + form.ingredient1.data

        if (form.ingredient2_quantity.data and form.ingredient2.data != "None"):
            ingredients_raw += ", " + str(form.ingredient2_quantity.data) + ":" + form.ingredient2.data
        if (form.ingredient3_quantity.data and form.ingredient3.data != "None"):
            ingredients_raw += ", " + str(form.ingredient3_quantity.data) + ":" + form.ingredient3.data
        if (form.ingredient4_quantity.data and form.ingredient4.data != "None"):
            ingredients_raw += ", " + str(form.ingredient4_quantity.data) + ":" + form.ingredient4.data
        if (form.ingredient5_quantity.data and form.ingredient5.data != "None"):
            ingredients_raw += ", " + str(form.ingredient5_quantity.data) + ":" + form.ingredient5.data

        ingredients, price = calculatePrice(ingredients_raw)
        post = Recipe(name=form.title.data, cook_time=form.cook_time.data, num_of_people=form.people_count.data, description=form.description.data, author=current_user, ingredients=ingredients, ingredients_raw=ingredients_raw, preperation=form.preperation.data, cooking=form.cooking.data, price=round((price/form.people_count.data),2))

        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect(url_for("home"))
    return render_template("create_post.html", title="New Post", form=form, legend="New Recipe")

# Summary: Renders a post with all it's details, as opposed to a preview. Not much done in the routing.
# TODO: Nothing.
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Recipe.query.get_or_404(post_id)
    return render_template("post.html", title=post.name, post=post)

# Summary: Fills the PostForm with the current users info for the GET, everything else is the same as the new_post.
# TODO: As I've said, this and the new_post is my worst work. Once I figure out how to do the ingredient situation better, I will fix both these routes.
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Recipe.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    user = User.query.filter_by(username=current_user.username).first_or_404()
    posts = Ingredient.query.filter_by(author=user)\
    .order_by(Ingredient.name.desc())
    ingredient_list = []
    ingredient_list.append(("None", ""))
    for ingredientChoices in posts:
        ing_id = ingredientChoices.name
        ing_name = ingredientChoices.name + " ("  + ingredientChoices.unit + ")"
        ing_info = (ing_id, ing_name)
        ingredient_list.append(ing_info)
    # Setting ingredient field choises to the user's ingredients
    form.ingredient1.choices = ingredient_list
    form.ingredient2.choices = ingredient_list
    form.ingredient3.choices = ingredient_list
    form.ingredient4.choices = ingredient_list
    form.ingredient5.choices = ingredient_list

    if form.validate_on_submit():
        ingredients_raw = str(form.ingredient1_quantity.data) + ":" + form.ingredient1.data

        if (form.ingredient2_quantity.data and form.ingredient2.data != "None"):
            ingredients_raw += ", " + str(form.ingredient2_quantity.data) + ":" + form.ingredient2.data
        if (form.ingredient3_quantity.data and form.ingredient3.data != "None"):
            ingredients_raw += ", " + str(form.ingredient3_quantity.data) + ":" + form.ingredient3.data
        if (form.ingredient4_quantity.data and form.ingredient4.data != "None"):
            ingredients_raw += ", " + str(form.ingredient4_quantity.data) + ":" + form.ingredient4.data
        if (form.ingredient5_quantity.data and form.ingredient5.data != "None"):
            ingredients_raw += ", " + str(form.ingredient5_quantity.data) + ":" + form.ingredient5.data

        ingredients, price = calculatePrice(ingredients_raw)

        post.name = form.title.data
        post.cook_time = form.cook_time.data
        post.num_of_people = form.people_count.data
        post.description = form.description.data
        post.ingredients_raw = ingredients_raw
        post.ingredients = ingredients
        post.preperation = form.preperation.data
        post.cooking = form.cooking.data
        post.price=round((price/form.people_count.data), 2)
        db.session.commit()
        flash("Your post has been updated!", "success")
        return redirect(url_for("post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.name
        form.cook_time.data = post.cook_time
        form.people_count.data = post.num_of_people
        form.description.data = post.description
        print("RAW ING:" + post.ingredients_raw)
        ingredient_entries = post.ingredients_raw.split(", ")
        form.ingredient1_quantity.data, form.ingredient1.data = ingredient_entries[0].split(":")
        try:
            if ingredient_entries[1]:
                form.ingredient2_quantity.data, form.ingredient2.data = ingredient_entries[1].split(":")
            if ingredient_entries[2]:
                form.ingredient3_quantity.data, form.ingredient3.data = ingredient_entries[2].split(":")
            if ingredient_entries[3]:
                form.ingredient4_quantity.data, form.ingredient4.data = ingredient_entries[3].split(":")
            if ingredient_entries[4]:
                form.ingredient5_quantity.data, form.ingredient5.data = ingredient_entries[4].split(":")
        except:
            print("whoops")

        form.preperation.data = post.preperation
        form.cooking.data = post.cooking
    return render_template("create_post.html", title="Update Post", form=form, legend="Update Post")

# Summary: Helper function that turns the raw ingredient data into something pretty, and adds up the prices. Returns a tuple: (pretty string, price)
    # e.g: Tomatoes:4, Yogurt: 100  -->  ("4 count of Tomatoes, 100 ml of Yogurt", $1.00)
# TODO: This works really well so far, but I'd rather deal with a list rather then storing the ingredients in a long string and parsing the info every time.
def calculatePrice(stri):
    total_price = 0
    pretty_string = ""
    for ingredient in stri.split(', '):
        ingredient_quantity, ingredient_name = ingredient.split(':')
        ing = Ingredient.query.filter_by(name=ingredient_name).first_or_404()
        price_of = float(ing.price) * float(ingredient_quantity)
        total_price += price_of
        price_str = str(round(price_of , 2))
        if ing.unit == "count":
            pretty_string += ingredient_quantity + " " + ingredient_name + " - " + price_str + ", "
        else:
            pretty_string += ingredient_quantity + " " + ing.unit + " of " + ingredient_name + " - $" + price_str + ", "

    return (pretty_string[:len(pretty_string)-2], total_price)

# Summary: Doesn't render any html, finds the post with the requested ID, deletes it from the database, redirects to home.
# TODO: Nothing.
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Recipe.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("home"))

# Summary: Does the same thing as the home route, but only shows the recipes for the requested user in the params.
# TODO: Nothing.
@app.route("/user/<string:username>")
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
@app.route("/ingredients/<string:username>", methods=['GET', 'POST'])
@login_required
def user_ingredients(username):
    form = IngredientForm()
    if form.validate_on_submit():
        pricePer = (form.price.data / form.amount.data)
        post = Ingredient(name=form.name.data, price=pricePer, unit=form.unit.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your Ingredient has been created!", "success")
        return redirect(url_for('user_ingredients', username=current_user.username))
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Ingredient.query.filter_by(author=user)\
    .order_by(Ingredient.name.desc())\
    .paginate(page=page, per_page=5)
    return render_template("ingredients.html", posts=posts, user=user, form=form)

# Summary: Same as the delete post route, but instead searches for the entry within the Ingredient database. Redirects to home.
# TODO: Nothing.
@app.route("/ingredient/<int:ingredient_id>/delete", methods=['POST'])
@login_required
def delete_ingredient(ingredient_id):
    post = Ingredient.query.get_or_404(ingredient_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your ingredient has been deleted!", "success")
    return redirect(url_for('user_ingredients', username=current_user.username))

# Summary: Helper function that sends an email to the requested user's email address, from douh.reset@gmail.com lol.
# TODO: Work on the email message, so it's a little nicer.
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='douh.reset@gmail.com', recipients=[user.email])
    msg.body = f''' To reset your password, click on the link below:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then just ignore this mail and no changes will be made.
    '''
    mail.send(msg)

# Summary: Page for letting the user enter an email, and then calling the send_reset_email function with that email.
# TODO: Maybe redesign, along with the other login/registeration stuff.
@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instuctions to reset your password", "info")
        return redirect(url_for('login'))
    return render_template("reset_request.html", title="Reset Password", form=form)

# Summary: This link is sent with the email, and if the received token isn't expired, then the user enters a new password.
# TODO: Nothing.
@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = User.verify_reset_token(token)
    if not user:
        flash("That is an invalid (or expired) token!", "warning")
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pass
        db.session.commit()
        flash(f"Password updated! You may now log in.", "success")
        return redirect(url_for("login"))
    return render_template("reset_token.html", title="Reset Password", form=form)
