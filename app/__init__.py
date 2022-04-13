from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['ENV'] = 'development'

    app.db = DB(app)
    login.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .article import bp as article_bp
    app.register_blueprint(article_bp)

    #We have to register the stock_pages.py to the blueprint!
    from .stock_pages import bp as stock_bp
    app.register_blueprint(stock_bp)

    from .purchases import bp as purchase_bp
    app.register_blueprint(purchase_bp)

    return app
