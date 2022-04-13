from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.purchase import Purchase

from flask import Blueprint

SORT_OPTIONS = ["ASC Ticker", "DESC Ticker", "ASC Time", "DESC Time"]


bp = Blueprint('purchases', __name__)

@bp.route('/exploreSearchPurchases', methods=['GET', 'POST'])
def explore_search():

    searchInput = request.form.get('searchInput')

    purchase_history = Purchase.get_by_search(current_user.id, searchInput)

    return render_template("pastPurchases.html", 
                            purchase_history=purchase_history, 
                            current_user=current_user,
                            sortOptions = SORT_OPTIONS,
                            searchInput=searchInput)

@bp.route('/pastPurchases', methods=['GET', 'POST'])
def explore():

    sortSelection = request.form.get('sort_select')

    sortSelection = 'ticker ASC' if sortSelection == 'ASC Ticker' else 'ticker DESC' if sortSelection == 'DESC Ticker' else 'time_purchased ASC' if sortSelection == 'ASC Time' else 'time_purchased DESC' 
    
    print("Index Sort Selection: " + sortSelection)

    purchase_history = Purchase.get_all_by_uid(current_user.id, sortSelection)

    return render_template("pastPurchases.html", 
                            purchase_history=purchase_history, 
                            current_user=current_user,
                            sortOptions = SORT_OPTIONS)

@bp.route('/pastPurchases', methods=['GET', 'POST'])
def purchases():
    # Get all stocks
    if not current_user.is_authenticated:
        return redirect(url_for('users.login', reasonForRedirect="You must login to view your purchase history."))

    return render_template("pastPurchases.html",    
                            purchase_history = Purchase.get_all_by_uid(current_user.id), 
                            current_user=current_user,
                            sortOptions = SORT_OPTIONS)