from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.article import Article
from .models.stock import Stock
from .models.stockDetail import StockDetail
from .models.user import User

from flask import Blueprint

bp = Blueprint('article', __name__)

SORT_OPTIONS = ["ASC Name", "DESC Name", "ASC Price", "DESC Price"]


@bp.route('/writeSubmit/<path:ticker>', methods=['GET', 'POST'])
def submit(ticker):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login', reasonForRedirect="You must login to write an article."))

    headline = request.form.get('headline')
    rating = request.form.get('rating')
    paragraph = request.form.get('text')
    Article.postArticle(ticker, current_user.id, int(rating), paragraph)

    return render_template("writeSubmit.html")


@bp.route('/write<path:ticker>', methods=['GET', 'POST'])
def write(ticker):
    # Get all stocks
    if not current_user.is_authenticated:
        return redirect(url_for('users.login', reasonForRedirect="You must login to write an article."))
    print("write article for: " + str(ticker))

    return render_template("writeArticle.html", ticker=ticker)
