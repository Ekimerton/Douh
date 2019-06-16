from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, AnyOf, InputRequired, Optional
from Driver.Models import User

# Summary: A registeration form that takes in a username, email and password. Checks that the username and email aren't in the system yet.
# TODO: Nothing.
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=5, max=15)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=99)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Continue")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username already taken!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email address already taken!')

# Summary: Just a simple login form.
# TODO: Nothing.
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Remember This Computer')
    submit = SubmitField("Continue")

# Summary: The form for updating the account information. The file types allowed for the pictures are 'jpg' and 'png'
# TODO: Nothing
class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=5, max=15)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username already taken!')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email address already taken!')

# Summary: The form for creating and updating posts.
# TODO: This is once again, very disgusting. I'd rather use one FormField for each ingredient, but wtfoms won't let me create a FormField with SelectFields.
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    cook_time = IntegerField("Cook Time", validators=[DataRequired()])
    people_count = IntegerField("People Count", validators=[DataRequired()])

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

    preperation = TextAreaField("Preperation Instuctions", validators=[DataRequired()])
    cooking = TextAreaField("Cooking Instuctions")
    submit = SubmitField("Post")

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

# Summary: The form for putting in an email for asking a reset, first makes sure the email is in the system.
# TODO: Nothing.
class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Send Reset Email Now!")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("That email address isn't registered!")

# Summary: The form for resetting passwords, just two password fields, and a submit button.
# TODO: Nothing.
class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=99)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])

    submit = SubmitField("Reset Password")
