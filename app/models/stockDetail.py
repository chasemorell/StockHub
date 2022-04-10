#Written by Chase Morell
#Work in progress

from flask import current_app as app

# most recent date the app has stock data downloaded. Update if we retrieve more current data.
MOST_RECENT_DATE_FOR_STOCK_PRICES = '2022-03-10'
OLDEST_DATE_FOR_STOCK_PRICES = '2020-03-12'

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
    def getDataBetweenDates(ticker,value,range):

        startDate = ""
        endDate = ""

        startArray = [int(x) for x in MOST_RECENT_DATE_FOR_STOCK_PRICES.split("-")]
        print("START ARRAY:")
        print(startArray)
        endDate = MOST_RECENT_DATE_FOR_STOCK_PRICES

        if range == '1 Day':
            if startArray[2] == 0:
                startArray[2] = 30
            else:
                startArray[2] = int(startArray[2]) - 1
        if range == '1 Week':
            if startArray[2] < 7:
                startArray[1] = startArray[1] - 1
                startArray[2] = 30-(7-startArray)
            else:
                startArray[2] = startArray[2] - 7

        if range == '1 Month':
            if startArray[1] != 1:
                startArray[1] = startArray[1] - 1
            else:
                startArray[1] = 12
        if range == '1 Year':
            startArray[0] = startArray[0] - 1
        if range == 'MAX':
            startArray = [int(x) for x in OLDEST_DATE_FOR_STOCK_PRICES.split("-")]

        print(startArray)
        for x in startArray:
            startDate = startDate + str(x) + "-"

        startDate = startDate[0:-1]
        print("STARTDATE: " + startDate)

        rows = app.db.execute('''
SELECT *
FROM timedata
WHERE ticker = :ticker AND period BETWEEN :sD AND :eD
''',
                              ticker=ticker,sD =startDate,eD = endDate )
        return [StockDetail(*row) for row in rows]

    def getColumnNames(self):
        rows = app.db.execute('''SELECT *
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = N\'timedata\'''')
        cNames = [x[3] for x in rows]
        cNames = [x for x in cNames if x != 'ticker']
        return cNames

