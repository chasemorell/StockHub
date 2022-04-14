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
    curPrice = Stock.get_current_price(ticker)
    shares_owned =0.0
    shares_owned_monetary_val=0
    login_flag = False
    stockOwned = False
    if current_user.is_authenticated:
        login_flag = True
        shares_detailed = Purchase.get_shares_quantity_money_val(current_user.id,ticker)
        if shares_detailed != []:
            shares_owned =shares_detailed[0][1]
            shares_owned_monetary_val =shares_detailed[0][2]
            # stockOwned = True
        portfolio = Purchase.get_user_portfolio(current_user.id)

        for stock in portfolio:
            if stock[1] == text:
                stockOwned = True

    return render_template('stockDetail.html', ticker=ticker, max=max(line_values), labels=line_labels,
                           values=line_values, generalData=generalData,graphValue = graphValue,
                           graphPeriod = graphPeriod,sGV = selectedGraphValue,sGP = selectedGraphPeriod,
                           articles = articles,articlesExist = articlesExist, stockOwned = stockOwned,curPrice=curPrice, shares_owned= shares_owned,shares_owned_monetary_val= shares_owned_monetary_val, login_flag=login_flag);

@bp.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    portfolio = Purchase.get_user_portfolio(current_user.id)
    if portfolio is None:
        portfolio = ""
    return render_template("portfolio.html", portfolio =  portfolio)

@bp.route('/transferMoney', methods=['GET'])
def transfer_money():
    return render_template('transfer_money.html')

@bp.route('/buystock', methods=['GET', 'POST'])
def buy_stock():
    ticker = request.args.get('ticker')
    if current_user.is_authenticated:
        type = int(request.form.get('buytype'))
        id = current_user.id
        amount = float(request.form.get('amntinfo'))

        if type == 1: #num_shares
            User.buy_stock(current_user.id,ticker, num_shares = amount)
        elif type == 2: #dollar_amount
            User.buy_stock(current_user.id,ticker, num_dollars=amount)
        else:
            print("Invalid Purchase Type")

        return redirect(url_for('stocks.portfolio'))
    else:
        return redirect(url_for('users.login', reasonForRedirect="You must login to buy a stock."))

@bp.route('/sellstock', methods=['GET', 'POST'])
def sell_stock():
    ticker = request.args.get('ticker')
    if current_user.is_authenticated:
        type = int(request.form.get('selltype'))
        id = current_user.id
        amount = float(request.form.get('amntinfo'))

        if type == 1: #num_shares
            User.sell_stock(current_user.id,ticker, num_shares = amount)
        elif type == 2: #dollar_amount
            User.sell_stock(current_user.id,ticker, num_dollars=amount)
        else:
            print("Invalid Purchase Type")

        return redirect(url_for('stocks.portfolio'))
    else:
        return redirect(url_for('users.login', reasonForRedirect="You must login to buy a stock."))
