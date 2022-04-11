#Written by Chase Morell
#Work in progress

from flask import current_app as app

# most recent date the app has stock data downloaded. Update if we retrieve more current data.
MOST_RECENT_DATE_FOR_STOCK_PRICES = '2022-03-10'
OLDEST_DATE_FOR_STOCK_PRICES = '2020-03-12'

class Article:
    def __init__(self, aid, uid, ticker,rating,article_text):
        self.aid = aid
        self.uid = uid
        self.ticker = ticker
        self.rating = rating
        self.article_text = article_text

    @staticmethod
    def get(id):
        rows = app.db.execute("""
        SELECT *
        FROM Articles
        WHERE aid = :id
        """,
                              id=id)
        return Article(*(rows[0])) if rows else None


    @staticmethod
    def getByTicker(ticker):
        rows = app.db.execute("""
                SELECT *
                FROM Articles
                WHERE ticker = :ticker
                """,
                              ticker=ticker)

        if rows:
            return [Article(*row) for row in rows]
        else:
            return None

    @staticmethod
    def postArticle(ticker,userId,rating,text):

        try:
            rows = app.db.execute("""
        INSERT INTO Articles(uid, ticker, rating,article_text)
        VALUES(:userId, :ticker, :rating, :text)
        RETURNING aid
        """,
                                  userId=userId,
                                  ticker=ticker,
                                  rating=rating,
                                  text=text)

            id = rows[0][0]
            return Article.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    def getColumnNames(self):
        rows = app.db.execute('''SELECT *
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = N\'timedata\'''')
        cNames = [x[3] for x in rows]
        cNames = [x for x in cNames if x != 'ticker']
        return cNames


