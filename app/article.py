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

    updateAid = request.args.get('updateAid')
    rating = request.form.get('rating')
    paragraph = request.form.get('text')

    if not (rating and paragraph):
        return redirect(url_for('article.write', ticker=ticker, reasonForRedirect="Error: Fill out all the forms!"))

    if not updateAid:
        Article.postArticle(ticker, current_user.id, int(rating), paragraph)
    else:
        Article.update_article(current_user.id,updateAid,int(rating),paragraph)
        return redirect(url_for('article.myArticles'))

    return render_template("writeSubmit.html")


@bp.route('/update/<path:aid>', methods=['GET', 'POST'])
def update(aid):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login', reasonForRedirect="You must login to write an article."))

    article = Article.get(aid)

    return render_template("writeArticle.html", ticker=article.ticker, article=article)


@bp.route('/write/<path:ticker>', methods=['GET', 'POST'])
def write(ticker, reasonForRedirect=""):
    reasonForRedirect = request.args.get('reasonForRedirect')

    if not current_user.is_authenticated:
        return redirect(url_for('users.login', reasonForRedirect="You must login to write an article."))
    print("write article for: " + str(ticker))

    return render_template("writeArticle.html", ticker=ticker, reasonForRedirect=reasonForRedirect)


@bp.route('/deleteArticle/<path:aid>/<path:uid>', methods=['GET', 'POST'])
def deleteArticle(aid, uid):
    # Get all stocks
    if not current_user.is_authenticated:
        return redirect(url_for('users.login', reasonForRedirect="You must login to write an article."))

    print("aid to delete: " + aid);
    print("uid to delete: " + uid);

    Article.delete_article(uid, aid)

    return redirect(url_for('article.myArticles'))


@bp.route('/myArticles', methods=['GET', 'POST'])
def myArticles():
    # Get all stocks
    if not current_user.is_authenticated:
        return redirect(url_for('users.login', reasonForRedirect="You must login to view your articles."))

    articles = Article.get_user_articles(current_user.id)

    return render_template("articles.html", articles=articles)
