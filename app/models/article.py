from flask import current_app as app


class Article:
    def __init__(self, article_id, user_id,ticker, rating,article_text):
        self.aid = article_id
        self.uid = user_id
        self.ticker = ticker
        self.rating = rating
        self.article_text = article_text

    @staticmethod
    def get(aid):
        rows = app.db.execute('''
        SELECT aid, uid,ticker, rating,article_text
        FROM Articles
        WHERE aid = :aid
        ''',
          aid = aid)
        return Article(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_user_articles(uid):
        rows = app.db.execute('''
        SELECT aid, uid,ticker, rating,article_text
        FROM Articles
        WHERE uid = :uid
        ''',
          uid = uid)
        return [Article(*row) for row in rows]

    @staticmethod
    def get_by_ticker(ticker):
        rows = app.db.execute('''
        SELECT aid, uid,ticker, rating,article_text
        FROM Articles
        WHERE ticker = :ticker
        ''',
           ticker = ticker)
        return [Article(*row) for row in rows]

    @staticmethod
    def update_article(uid,aid,rating,article_text):
        rows = app.db.execute('''
        UPDATE Articles
        SET rating = :rating, article_text=:article_text
        WHERE uid = :uid and aid = :aid
        RETURNING article_id
        ''',
           uid = uid, aid=aid)
        return Article.get(aid)


    @staticmethod
    def delete_article(uid,aid):
        rows = app.db.execute('''
        DELETE FROM Articles
        WHERE uid = :uid and aid = :aid
        ''',
           uid = uid, aid=aid)
        return
