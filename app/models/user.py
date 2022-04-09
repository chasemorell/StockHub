from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

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
