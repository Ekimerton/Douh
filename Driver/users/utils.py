import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from Driver import mail

# Summary: A helper function for saving pictures. Takes in the image file, gives it a random hexadecimal name, and saves it in the static folder.
# TODO: Nothing.
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125 ,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

# Summary: Helper function that sends an email to the requested user's email address, from douh.reset@gmail.com lol.
# TODO: Work on the email message, so it's a little nicer.
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='douh.reset@gmail.com', recipients=[user.email])
    msg.body = f''' To reset your password, click on the link below:
    {url_for('users.reset_token', token=token, _external=True)}
    If you did not make this request then just ignore this mail and no changes will be made.
    '''
    mail.send(msg)
