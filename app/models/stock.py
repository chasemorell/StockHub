from flask import current_app as app


class Stock:
    def __init__(self, ticker, name,sector, price):
        self.ticker = ticker
        self.name = name
        self.sector = sector
        self.price = price

    @staticmethod
    def get(ticker):
        rows = app.db.execute('''
        SELECT ticker, name,sector, price
        FROM Stocks
        WHERE ticker = :ticker
        ''',
          ticker = ticker)
        return Stock(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_by_sector(sector):
        rows = app.db.execute('''
        SELECT id, ticker,name, sector, price
        FROM Stocks
        WHERE sector = :sector
        ''',
           sector = sector)
        return [Stock(*row) for row in rows]
