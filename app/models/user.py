from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from .. import login


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.available_balance =0
        self.portfolio_value = 0

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
        SELECT password, id, email, firstname, lastname
        FROM Users
        WHERE email = :email
        """, email=email )
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
        SELECT email
        FROM Users
        WHERE email = :email
        """,
            email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname):
        try:
            rows = app.db.execute(""" INSERT INTO
                Users(email, password, firstname, lastname,available_balance,portfolio_value)
                VALUES(:email, :password, :firstname, :lastname,0,0)
                RETURNING id
                """,
                  email=email,
                  password=generate_password_hash(password),
                  firstname=firstname,
                  lastname=lastname)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
            SELECT id, email, firstname, lastname
            FROM Users
            WHERE id = :id
            """, id=id)
        return User(*(rows[0])) if rows else None

    @staticmethod
    def deposit(id,quantity):
        rows = app.db.execute("""
            UPDATE Users
            SET available_balance = available_balance + :quanity
            WHERE id = :id
            """,
              id=id,
              quanity=quantity)
        return User.get(id)

    @staticmethod
    def update_portfolio_value(id):
        rows = app.db.execute("""
            SELECT id,sum(monetary_value)
            FROM Accounts
            WHERE id = :id
            GROUP BY id
            """,
              id=id)
        cur_sum  = rows[0][1]
        update_money = app.db.execute("""
            UPDATE Users
            SET portfolio_value = available_balance + :cur_sum
            WHERE id = :id
            RETURNING id
            """,
              id=id,
              portfolio_value = cur_sum)

        return User.get(id)

    @staticmethod
    def buy_stock(uid, ticker, num_shares=False, num_dollars=False):
        if not num_shares and not num_dollars:
            return

        #info = Stock.get_in
        elif num_shares:
            cur_price = Stock.get_current_price(ticker)
            shares_cost= num_shares*cur_price

        elif num_dollars:
            cur_price = Stock.get_current_price(ticker)
            shares_cost= num_dollars/cur_price

        time_stamp = datetime.now()
        buy_stock = app.db.execute("""
            INSERT INTO
            Purchases(uid, ticker,num_shares,cost, time_purchased)
            VALUES(:uid, :ticker, :num_shares, :cost :time_stamp)
            RETURNING uid
            """,
            uid= uid,
            ticker=ticker,
            cost = shares_cost,
            num_shares = num_shares,
            time_stamp = timestamp)

        cur_user= update_portfolio_value(uid)

        return cur_user

    def sell_stock(uid, ticker, num_shares=False, num_dollars=False):
        if not num_shares and not num_dollars:
            return
        # elif if num_shares:
        #     buy_stock(uid, ticker,-1*num_shares)
        # elif if num_dollars:
        #     buy_stock(uid, ticker,-1*num_dollars)
        #

        user_ticker_info = app.db.execute("""
            SELECT ticker,sum(num_shares),sum(cost)
            FROM Purchases
            WHERE id = :uid AND ticker =:ticker
            GROUP BY ticker
            """,
            uid= uid,
            ticker=ticker
            )
        if not user_ticker_info:
            print('You do not own this ticker')
            return
        num_shares = user_ticker_info[0][1]
        shares_value = user_ticker_info[0][2]
        time_stamp = datetime.now()


        if num_shares:
            cur_price = Stock.get_current_price(ticker)
            shares_cost= num_shares*cur_price

        elif num_dollars:
            cur_price = Stock.get_current_price(ticker)
            shares_cost= num_dollars/cur_price

        sell_stock = app.db.execute("""
            INSERT INTO
            Purchases(uid, ticker,num_shares,cost, time_purchased)
            VALUES(:uid, :ticker, -1*:num_shares, -1*:cost :time_stamp)
            RETURNING uid
            """,
            uid= uid,
            ticker=ticker,
            cost = shares_cost,
            num_shares = num_shares,
            time_stamp = timestamp)

        cur_user= update_portfolio_value(uid)
        return cur_user
