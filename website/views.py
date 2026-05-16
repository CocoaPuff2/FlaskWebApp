# store routes for website (pages, anything but login)

from flask import Blueprint, render_template
from flask_login import  login_required, current_user

# define that this file is a blueprint aka bunch of roots/urls 
views = Blueprint('views', __name__)

@views.route('/') #url for home page
@login_required
def home():
    return render_template("home.html", user=current_user)

