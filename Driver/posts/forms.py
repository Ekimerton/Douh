from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired, InputRequired, Optional, ValidationError

# Summary: The form for creating and updating posts.
# TODO: This is once again, very disgusting. I'd rather use one FormField for each ingredient, but wtfoms won't let me create a FormField with SelectFields.
class PostForm(FlaskForm):
    title = StringField("Title*", validators=[DataRequired()])
    description = TextAreaField("Description*", validators=[DataRequired()])
    cook_time = IntegerField("Time(min)*", validators=[DataRequired()])
    people_count = IntegerField("People*", validators=[DataRequired()])

    ingredient1 = SelectField('Ingredient', choices=[], validators=[InputRequired()])
    ingredient1_quantity = FloatField('Amount', validators=[InputRequired()])
    ingredient2 = SelectField('Ingredient', choices=[], validators=[Optional()])
    ingredient2_quantity = FloatField('Amount', validators=[Optional()])
    ingredient3 = SelectField('Ingredient', choices=[], validators=[Optional()])
    ingredient3_quantity = FloatField('Amount', validators=[Optional()])
    ingredient4 = SelectField('Ingredient', choices=[], validators=[Optional()])
    ingredient4_quantity = FloatField('Amount', validators=[Optional()])
    ingredient5 = SelectField('Ingredient', choices=[], validators=[Optional()])
    ingredient5_quantity = FloatField('Amount', validators=[Optional()])
    ingredient6 = SelectField('Ingredient', choices=[], validators=[Optional()])
    ingredient6_quantity = FloatField('Amount', validators=[Optional()])
    ingredient7 = SelectField('Ingredient', choices=[], validators=[Optional()])
    ingredient7_quantity = FloatField('Amount', validators=[Optional()])
    ingredient8 = SelectField('Ingredient', choices=[], validators=[Optional()])
    ingredient8_quantity = FloatField('Amount', validators=[Optional()])
    ingredient9 = SelectField('Ingredient', choices=[], validators=[Optional()])
    ingredient9_quantity = FloatField('Amount', validators=[Optional()])
    ingredient10 = SelectField('Ingredient', choices=[], validators=[Optional()])
    ingredient10_quantity = FloatField('Amount', validators=[Optional()])

    preperation = TextAreaField("Preperation Instuctions*", validators=[DataRequired()])
    cooking = TextAreaField("Cooking Instuctions")
    submit = SubmitField("Post")

    def validate_ingredient1(self, ingredient1):
        print(ingredient1.data)
        if ingredient1.data == "None":
            raise ValidationError('You must add at least one ingredient!')

# Summary: The form that is rendered with the ingredients.html. The unitTypes are stored in an array of tuples.
# TODO: Add conversion between different unit types.
class IngredientForm(FlaskForm):
    unitTypes = [('mL', 'millilitres'),
                 ('g', 'grams'),
                 ('cups', 'cups'),
                 ('tsp', 'teaspoons'),
                 ('tbsp', 'tablespoons'),
                 ('count', 'count')]

    name = StringField("Name", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    amount = IntegerField("Amount", validators=[DataRequired()])
    unit = SelectField("Unit", validators=[DataRequired()], choices=unitTypes)
    submit = SubmitField("Create Ingredient")
