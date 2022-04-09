#Written by Chase Morell
from flask import current_app as app

# most recent date the app has stock data downloaded. Update if we retrieve more current data.
MOST_RECENT_DATE_FOR_STOCK_PRICES = '2022-03-10'


class Stock:
    def __init__(self, ticker, name, sector,price):
        self.ticker = ticker
        self.name = name
        self.sector = sector
        self.price = price


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
    def get_all(sortBy):
        print("get all")
        print(sortBy)

        if sortBy == "ASC Name":
            rows = app.db.execute('''
SELECT stocks.ticker,name,sector,closeprice
FROM stocks
JOIN (SELECT ticker AS ticker,closeprice
FROM timedata
WHERE  period = :p
ORDER BY period) AS tickerPrice ON tickerPrice.ticker = stocks.ticker
ORDER BY name ASC
''', p=MOST_RECENT_DATE_FOR_STOCK_PRICES
                                  )
        elif sortBy == "DESC Name":
            rows = app.db.execute('''
            SELECT stocks.ticker,name,sector,closeprice
FROM stocks
JOIN (SELECT ticker AS ticker,closeprice
FROM timedata
WHERE  period = :p
ORDER BY period) AS tickerPrice ON tickerPrice.ticker = stocks.ticker
ORDER BY name DESC
            ''', p=MOST_RECENT_DATE_FOR_STOCK_PRICES
                                  )

        elif sortBy == "ASC Price":
            rows = app.db.execute('''
                        SELECT stocks.ticker,name,sector,closeprice
            FROM stocks
            JOIN (SELECT ticker AS ticker,closeprice
            FROM timedata
            WHERE  period = :p
            ORDER BY period) AS tickerPrice ON tickerPrice.ticker = stocks.ticker
            ORDER BY closeprice ASC
                        ''', p=MOST_RECENT_DATE_FOR_STOCK_PRICES
                                  )

        elif sortBy == "DESC Price":
            rows = app.db.execute('''
                        SELECT stocks.ticker,name,sector,closeprice
            FROM stocks
            JOIN (SELECT ticker AS ticker,closeprice
            FROM timedata
            WHERE  period = :p
            ORDER BY period) AS tickerPrice ON tickerPrice.ticker = stocks.ticker
            ORDER BY closeprice DESC
                        ''', p=MOST_RECENT_DATE_FOR_STOCK_PRICES
                                  )

        return [Stock(*row) for row in rows]

    @staticmethod
    def get_by_search(searchInput):
        sqlSearchInput = '%' + searchInput + '%'
        print(sqlSearchInput)
        rows = app.db.execute('''
        SELECT stocks.ticker,name,sector,closeprice
FROM stocks
JOIN (SELECT ticker AS ticker,closeprice
FROM timedata
WHERE  period = :p
ORDER BY period) AS tickerPrice ON tickerPrice.ticker = stocks.ticker
WHERE name ILIKE :s OR stocks.ticker ILIKE :s
ORDER BY name DESC ''', s=sqlSearchInput, p = MOST_RECENT_DATE_FOR_STOCK_PRICES

                              )
        return [Stock(*row) for row in rows]

    #TODO: This function is a work in progress and doesn't work
    def get_details_by_ticker(ticker):
        rows = app.db.execute('''
                SELECT stocks.ticker,name,sector,closeprice
        FROM stocks
        JOIN (SELECT ticker AS ticker,closeprice
        FROM timedata
        WHERE  period = :p
        ORDER BY period) AS tickerPrice ON tickerPrice.ticker = stocks.ticker
        WHERE name ILIKE :s OR stocks.ticker ILIKE :s
        ORDER BY name DESC ''', s=sqlSearchInput, p=MOST_RECENT_DATE_FOR_STOCK_PRICES

                              )
        return [Stock(*row) for row in rows]
