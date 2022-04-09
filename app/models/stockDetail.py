#Written by Chase Morell
#Work in progress

from flask import current_app as app

# most recent date the app has stock data downloaded. Update if we retrieve more current data.
MOST_RECENT_DATE_FOR_STOCK_PRICES = '2022-03-10'


class StockDetail:
    def __init__(self, ticker, period, closeprice,highprice,lowprice,transactioncount,openprice,tradingvolume,volumeweightedaverageprice):
        self.ticker = ticker
        self.period = period
        self.closeprice = closeprice
        self.highprice = highprice
        self.lowprice = lowprice
        self.transactioncount = transactioncount
        self.openprice = openprice
        self.tradingvolume = tradingvolume
        self.volumeweightedaverageprice = volumeweightedaverageprice



    @staticmethod
    def getDataBetweenDates(ticker):
        rows = app.db.execute('''
SELECT *
FROM timedata
WHERE ticker = :ticker
''',
                              ticker=ticker)
        return [StockDetail(*row) for row in rows]
