from flask import current_app as app


class Stock:
    def __init__(self, ticker, name, sector):
        self.ticker = ticker
        self.name = name
        self.sector = sector

    @staticmethod
    def get(ticker):
        rows = app.db.execute('''
SELECT ticker, name, sector
FROM Stocks
WHERE ticker = :ticker
''',
                              ticker=ticker)
        return Stock(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT ticker, name, sector
FROM Stocks
'''
                             )
        return [Stock(*row) for row in rows]
