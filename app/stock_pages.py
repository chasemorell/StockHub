from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.stock import Stock
from .models.stockDetail import StockDetail
from .models.user import User

from flask import Blueprint

bp = Blueprint('stocks', __name__)

SORT_OPTIONS = ["ASC Name", "DESC Name","ASC Price","DESC Price"]


@bp.route('/explore', methods=['GET', 'POST'])
def explore():
    # Get all stocks
    sortSelection = request.form.get('sort_select')

    if not sortSelection:
        sortSelection = "ASC Name"
    print("Index Sort Selection: " + sortSelection)
    stocks = Stock.get_all(sortSelection)

    return render_template("stockExplore.html", stocks=stocks, sortOptions=SORT_OPTIONS, selectedSort=sortSelection,
                           searchInput="")

@bp.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    # Get all stocks
    sortSelection = request.form.get('sort_select')

    if not sortSelection:
        sortSelection = "ASC Name"
    print("Index Sort Selection: " + sortSelection)
    stocks = Stock.get_all(sortSelection)

    return render_template("portfolio.html", stocks=stocks, sortOptions=SORT_OPTIONS, selectedSort=sortSelection,
                           searchInput="")


@bp.route('/exploreSearch', methods=['GET', 'POST'])
def explore_search():
    searchInput = request.form.get('searchInput')
    stocks = Stock.get_by_search(searchInput)
    return render_template("stockExplore.html", stocks=stocks, sortOptions=SORT_OPTIONS, selectedSort="ASC",
                           searchInput=searchInput)


@bp.route('/stock/<path:text>', methods=['GET'])
def stock(text):
    ticker = text
    print("Ticker is: " + ticker)


    timedata = StockDetail.getDataBetweenDates(ticker)
    print(timedata[0].openprice)

    line_labels = [x.period for x in timedata]
    line_values = [x.closeprice for x in timedata]

    return render_template('stockDetail.html', title=ticker, max=max(line_values), labels=line_labels, values=line_values);

@bp.route('/transferMoney', methods=['GET'])
def transfer_money():
    return render_template('transfer_money.html')