from app import create_app

app = create_app()

'''
from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

#from flask import Flask, redirect, url_for, render_template
"""
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/stocks")
def stocks():
    return render_template("stocks.html")

@app.route("/user")
def user():
    return render_template("user.html")

if __name__ == "__main__":
    app.run()
'''
