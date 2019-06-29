from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from Driver import db
from Driver.models import Recipe, Ingredient, User
from Driver.posts.forms import PostForm

posts = Blueprint('posts', __name__)

# Route for creating new posts, currently handles 10 ingredients.
# TODO: Honestly, this - and the update_post routes are my worst work in this project. The code looks horrible, could work better, but it gets the work done for now. I'd also like to add markdown support for the text fields.
@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    user = User.query.filter_by(username=current_user.username).first_or_404()
    posts = Ingredient.query.filter_by(author=user)\
    .order_by(Ingredient.id.desc())
    ingredient_list = []
    ingredient_list.append(("None", ""))
    for post in posts:
        ing_id = str(post.id)
        ing_name = post.name + " ("  + post.unit + ")"
        ing_info = (ing_id, ing_name)
        ingredient_list.append(ing_info)
    # Setting ingredient field choises to the user's ingredients
    form.ingredient1.choices = ingredient_list
    form.ingredient2.choices = ingredient_list
    form.ingredient3.choices = ingredient_list
    form.ingredient4.choices = ingredient_list
    form.ingredient5.choices = ingredient_list
    form.ingredient6.choices = ingredient_list
    form.ingredient7.choices = ingredient_list
    form.ingredient8.choices = ingredient_list
    form.ingredient9.choices = ingredient_list
    form.ingredient10.choices = ingredient_list

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
        if (form.ingredient6_quantity.data and form.ingredient6.data != "None"):
            ingredients_raw += ", " + str(form.ingredient6_quantity.data) + ":" + form.ingredient6.data
        if (form.ingredient7_quantity.data and form.ingredient7.data != "None"):
            ingredients_raw += ", " + str(form.ingredient7_quantity.data) + ":" + form.ingredient7.data
        if (form.ingredient8_quantity.data and form.ingredient8.data != "None"):
            ingredients_raw += ", " + str(form.ingredient8_quantity.data) + ":" + form.ingredient8.data
        if (form.ingredient9_quantity.data and form.ingredient9.data != "None"):
            ingredients_raw += ", " + str(form.ingredient9_quantity.data) + ":" + form.ingredient9.data
        if (form.ingredient10_quantity.data and form.ingredient10.data != "None"):
            ingredients_raw += ", " + str(form.ingredient10_quantity.data) + ":" + form.ingredient10.data

        ingredients, price = calculatePrice(ingredients_raw)
        post = Recipe(name=form.title.data, cook_time=form.cook_time.data, num_of_people=form.people_count.data, description=form.description.data, author=current_user, ingredients=ingredients, ingredients_raw=ingredients_raw, preperation=form.preperation.data, cooking=form.cooking.data, price=round((price/form.people_count.data),2))

        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect(url_for("main.home"))
    return render_template("create_post.html", title="New Post", form=form, legend="New Recipe")

# Summary: Renders a post with all it's details, as opposed to a preview. Not much done in the routing.
# TODO: Nothing.
@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Recipe.query.get_or_404(post_id)
    return render_template("post.html", title=post.name, post=post)

# Summary: Fills the PostForm with the current users info for the GET, everything else is the same as the new_post.
# TODO: As I've said, this and the new_post is my worst work. Once I figure out how to do the ingredient situation better, I will fix both these routes.
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Recipe.query.get_or_404(post_id)
    if post.author != current_user or current_user.username != "Ekimerton":
        abort(403)
    form = PostForm()
    user = User.query.filter_by(username=current_user.username).first_or_404()
    posts = Ingredient.query.filter_by(author=user)\
    .order_by(Ingredient.name.desc())
    ingredient_list = []
    ingredient_list.append(("None", ""))
    for ingredientChoices in posts:
        ing_id = str(ingredientChoices.id)
        ing_name = ingredientChoices.name + " ("  + ingredientChoices.unit + ")"
        ing_info = (ing_id, ing_name)
        ingredient_list.append(ing_info)

    # Setting ingredient field choises to the user's ingredients
    form.ingredient1.choices = ingredient_list
    form.ingredient2.choices = ingredient_list
    form.ingredient3.choices = ingredient_list
    form.ingredient4.choices = ingredient_list
    form.ingredient5.choices = ingredient_list
    form.ingredient6.choices = ingredient_list
    form.ingredient7.choices = ingredient_list
    form.ingredient8.choices = ingredient_list
    form.ingredient9.choices = ingredient_list
    form.ingredient10.choices = ingredient_list

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
        if (form.ingredient6_quantity.data and form.ingredient6.data != "None"):
            ingredients_raw += ", " + str(form.ingredient6_quantity.data) + ":" + form.ingredient6.data
        if (form.ingredient7_quantity.data and form.ingredient7.data != "None"):
            ingredients_raw += ", " + str(form.ingredient7_quantity.data) + ":" + form.ingredient7.data
        if (form.ingredient8_quantity.data and form.ingredient8.data != "None"):
            ingredients_raw += ", " + str(form.ingredient8_quantity.data) + ":" + form.ingredient8.data
        if (form.ingredient9_quantity.data and form.ingredient9.data != "None"):
            ingredients_raw += ", " + str(form.ingredient9_quantity.data) + ":" + form.ingredient9.data
        if (form.ingredient10_quantity.data and form.ingredient10.data != "None"):
            ingredients_raw += ", " + str(form.ingredient10_quantity.data) + ":" + form.ingredient10.data

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
        return redirect(url_for("posts.post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.name
        form.cook_time.data = post.cook_time
        form.people_count.data = post.num_of_people
        form.description.data = post.description
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
            if ingredient_entries[5]:
                form.ingredient6_quantity.data, form.ingredient6.data = ingredient_entries[5].split(":")
            if ingredient_entries[6]:
                form.ingredient7_quantity.data, form.ingredient7.data = ingredient_entries[6].split(":")
            if ingredient_entries[7]:
                form.ingredient8_quantity.data, form.ingredient8.data = ingredient_entries[7].split(":")
            if ingredient_entries[8]:
                form.ingredient9_quantity.data, form.ingredient9.data = ingredient_entries[8].split(":")
            if ingredient_entries[9]:
                form.ingredient8_quantity.data, form.ingredient8.data = ingredient_entries[9].split(":")
            if ingredient_entries[10]:
                form.ingredient9_quantity.data, form.ingredient9.data = ingredient_entries[10].split(":")
            if ingredient_entries[11]:
                form.ingredient10_quantity.data, form.ingredient10.data = ingredient_entries[11].split(":")
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
        ingredient_quantity, ingredient_id = ingredient.split(':')
        ing = Ingredient.query.filter_by(id=ingredient_id).first_or_404()
        price_of = float(ing.price) * float(ingredient_quantity)
        total_price += price_of
        price_str = str(round(price_of , 2))
        if ing.unit == "count":
            pretty_string += ingredient_quantity + " " + ing.name + " - $" + price_str + ", "
        else:
            pretty_string += ingredient_quantity + " " + ing.unit + " of " + ing.name + " - $" + price_str + ", "

    return (pretty_string[:len(pretty_string)-2], total_price)

# Summary: Doesn't render any html, finds the post with the requested ID, deletes it from the database, redirects to home.
# TODO: Nothing.
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Recipe.query.get_or_404(post_id)
    if post.author != current_user or current_user.username != "Ekimerton":
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("main.home"))
