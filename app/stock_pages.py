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
from .models.purchase import Purchase

from flask import Blueprint

bp = Blueprint('stocks', __name__)

SORT_OPTIONS = ["ASC Name", "DESC Name", "ASC Price", "DESC Price"]

@bp.route('/', methods=['GET'])
def home():
    return render_template("index.html")

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


@bp.route('/exploreSearch', methods=['GET', 'POST'])
def explore_search():
    searchInput = request.form.get('searchInput')
    stocks = Stock.get_by_search(searchInput)
    return render_template("stockExplore.html", stocks=stocks, sortOptions=SORT_OPTIONS, selectedSort="ASC",
                           searchInput=searchInput)

@bp.route('/stock/<path:text>', methods=['GET','POST'])
def stock(text):

    selectedGraphValue = request.form.get('graphValue')
    selectedGraphPeriod = request.form.get('graphPeriod')

    if(selectedGraphPeriod == None or selectedGraphPeriod == None):
        selectedGraphValue = 'closeprice'
        selectedGraphPeriod = '1 Month'

    print(selectedGraphValue)
    print(selectedGraphPeriod)

    ticker = text
    print("Ticker is: " + ticker)

    timedata = StockDetail.getDataBetweenDates(ticker, selectedGraphValue, selectedGraphPeriod)
    generalData = Stock.get(ticker)

    articles = Article.getByTicker(ticker)
    articlesExist = True
    if articles == None:
        print("there are no articles for this stock")
        articlesExist = False

    line_labels = [x.period for x in timedata]

    if selectedGraphValue == 'closeprice':
        line_values = [x.closeprice for x in timedata]
    elif selectedGraphValue == 'highprice':
        line_values = [x.highprice for x in timedata]
    elif selectedGraphValue == 'lowprice':
        line_values = [x.lowprice for x in timedata]
    elif selectedGraphValue == 'transactioncount':
        line_values = [x.transactioncount for x in timedata]
    elif selectedGraphValue == 'openprice':
        line_values = [x.openprice for x in timedata]
    elif selectedGraphValue == 'tradingvolume':
        line_values = [x.tradingvolume for x in timedata]
    elif selectedGraphValue == 'volumeweightedaverageprice':
        line_values = [x.volumeweightedaverageprice for x in timedata]
    else:
        line_values = [x.closeprice for x in timedata]


    graphValue = StockDetail.getColumnNames(None)

    graphPeriod = ["1 Day", "1 Week", "1 Month","1 Year","MAX"]

    portfolio = Purchase.get_user_portfolio(current_user.id)
    flag = 0
    for stock in portfolio:
        if stock[1] == text:
            flag = 1
    
    if flag == 1:
        stockOwned = True
    else:
        stockOwned = False

    return render_template('stockDetail.html', ticker=ticker, max=max(line_values), labels=line_labels,
                           values=line_values, generalData=generalData,graphValue = graphValue,
                           graphPeriod = graphPeriod,sGV = selectedGraphValue,sGP = selectedGraphPeriod,
                           articles = articles,articlesExist = articlesExist, stockOwned = stockOwned);

@bp.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    portfolio = Purchase.get_user_portfolio(current_user.id)
    if portfolio is None:
        portfolio = ""     
    return render_template("portfolio.html", portfolio =  portfolio)

@bp.route('/transferMoney', methods=['GET'])
def transfer_money():
    return render_template('transfer_money.html')
