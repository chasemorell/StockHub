from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from .stock import Stock
from .purchase import Purchase
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

    @staticmethod
    def get_available_balance(id):
        rows = app.db.execute("""
            SELECT available_balance
            FROM Users
            WHERE id = :id
            """, id=id)

        res = rows[0][0]

        return res


    @staticmethod
    def withdraw(id,quantity):
        rows = app.db.execute("""
            UPDATE Users
            SET
                available_balance = CASE WHEN available_balance - :quanity >0 THEN  available_balance - :quanity
                ELSE
                    0
                END
            WHERE id = :id
            RETURNING available_balance
            """,
              id=id,
              quanity=quantity)
        return rows

    # @staticmethod
    # def update_portfolio_value(id):
    #     current_portfolio_sum= 0
    #     update_money = app.db.execute("""
    #         UPDATE Users
    #         SET portfolio_value = available_balance + :cur_sum
    #         WHERE id = :id
    #         RETURNING id
    #         """,
    #           id=id,
    #           portfolio_value = cur_sum)
    #
    #     return User.get(id)

    @staticmethod
    def buy_stock(uid, ticker, num_shares=False, num_dollars=False):
        if not num_shares and not num_dollars:
            return

        #info = Stock.get_in
        elif num_shares:
            cur_price = Stock.get_current_price(ticker)
            num_dollars= num_shares*cur_price

        elif num_dollars:
            cur_price = Stock.get_current_price(ticker)
            num_shares= num_dollars/cur_price


        current_balance = User.get_available_balance(uid)
        if  current_balance < num_dollars:
            return
        else:
            cur_time_stamp = datetime.now()
            buy_stock = app.db.execute("""
                INSERT INTO
                Purchases(uid, ticker,num_shares,cost, time_purchased)
                VALUES(:uid, :ticker, :num_shares, :cost, :time_stamp)
                RETURNING uid
                """,
                uid= uid,
                ticker=ticker,
                cost = num_dollars,
                num_shares = num_shares,
                time_stamp = cur_time_stamp)



    @staticmethod
    def sell_stock(uid, ticker, num_shares=False, num_dollars=False):
        if not num_shares and not num_dollars:
            return

        time_stamp = datetime.now()


        if num_shares:
            cur_price = Stock.get_current_price(ticker)
            num_dollars= num_shares*cur_price

        elif num_dollars:
            cur_price = Stock.get_current_price(ticker)
            num_shares= num_dollars/cur_price


        shares_detailed = Purchase.get_shares_quantity_money_val(uid,ticker)
        if shares_detailed != []:
            shares_owned =shares_detailed[0][1]
            shares_owned_monetary_val =shares_detailed[0][2]

        if  shares_owned < num_shares or shares_owned_monetary_val < num_dollars:
            return

        sell_stock = app.db.execute("""
            INSERT INTO
            Purchases(uid, ticker,num_shares,cost, time_purchased)
            VALUES(:uid, :ticker, -1*:num_shares, -1*:cost, :time_stamp)
            RETURNING uid
            """,
            uid= uid,
            ticker=ticker,
            cost = num_dollars,
            num_shares = num_shares,
            time_stamp = time_stamp)

        update_money = app.db.execute("""
                UPDATE Users
                SET available_balance = available_balance + :num_dollars
                WHERE id = :uid
                """,
                  uid=uid,
                  num_dollars = num_dollars)

        return
