# 2022 Chase Morell

import pandas as pd
import requests
import json
import pickle
import time
import psycopg2
import datetime
import sys

apiKeys = ["k_ePxQg21brxYpfaTJ0vNPFH3iqS3MeD", "Nt89WhIX9zlxMA2wmgIPNkrzLoBiOjYf", "E3va20jCegrw0s25IzTn0V7RoD5xEhk7",
           "VqxYiXemp8gz0luabgtnujOJJd0m3kad", "li0kMCbq8VFfqab5gaQbTp0h3ATfSuSa"]

#tickerYTDFile = "./db/data/tickerYTD.obj"
#sp500 = pd.read_csv("./db/data/sp500.csv")

# print(json.dumps(response, indent=2))

tickerEntries = []


# Given a dataframe of stocks, get daily market info for each stock between given dates
# Stocks parameter must be of type pandas dataframe and MUST have row 'Symbol'
def getDailyTickerDataBetweenDates(stocks, dateStart, dateEnd):
    responseList = []
    for index, row in stocks.iterrows():
        print(index)
        print(row['Symbol'])
        ticker = row['Symbol']
        aI = index % len(apiKeys)
        request = "https://api.polygon.io/v2/aggs/ticker/" + ticker + "/range/1/day/" + dateStart + "/" + dateEnd + "?adjusted=true&sort=asc&apiKey=" + \
                  apiKeys[aI]
        response = requests.get(request)
        response = response.json()
        responseText = str(response)
        if not (("error" in responseText) or ("Error" in responseText)):
            print("response ok")
        print(response["resultsCount"])
        # print(str(response))
        responseList.append(response)
        time.sleep(2.6)
    return responseList


# Given a pathname and python object, saves object to pathname
# Helpful to cache API responses
def pickleFile(path, obj):
    filehandler = open(path, 'wb')
    pickle.dump(obj, filehandler)
    return True


# Restores a pickled object saved at path
def restorePickledFile(path):
    file = open(path, 'rb')
    obj = pickle.load(file)
    return obj


# Given a dataframe of stocks, adds stocks (ticker,name sector) to SQL database
# This doesn't have any price data
def addStocks(stocks):
    conn = psycopg2.connect("dbname=stockhub user=user password=516")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    for index, row in stocks.iterrows():
        try:
            cur.execute("""INSERT INTO Stocks (ticker, name,sector)
                    VALUES (%s, %s, %s)
                    """, (row["Symbol"], row["Name"], row["Sector"]))
        except Exception as error:
            print("Oops! An exception has occured:", error)
            print("Exception TYPE:", type(error))

    cur.close()
    # commit the changes
    conn.commit()


# Given a json from polygon.io api, add each time entry for every stock to SQL database
def addTimeData(timeData):
    conn = psycopg2.connect("dbname=stockhub user=user password=516")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    i = 0
    for stock in timeData:

        for period in stock["results"]:
            print(len(period))
            timeFormatted = datetime.datetime.fromtimestamp(period["t"] / 1000)
            print(i)
            try:
                cur.execute("""INSERT INTO timedata (ticker, period,closeprice,highprice,lowprice,transactioncount,openprice,tradingvolume,volumeweightedaverageprice)
                    VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s)
                    """, (stock["ticker"], timeFormatted.date(), round(period["c"], 2), round(period["h"], 2),
                          round(period["l"], 2), period["n"], round(period["o"], 2), round(period["v"], 2),
                          round(period["vw"], 2)))
            except Exception as error:
                print("Oops! An exception has occured:", error)
                print("Exception TYPE:", type(error))

    cur.close()
    # commit the changes
    conn.commit()


startDate = "2020-03-10"
endDate = "2022-03-10"

def doA(rootPath):
    tickerYTDFile = rootPath + "/data/tickerYTD.obj"
    sp500 = pd.read_csv(rootPath + "/data/sp500.csv")

    addStocks(sp500);
    tickerEntries = restorePickledFile(tickerYTDFile)
    addTimeData(tickerEntries)


def doF():
    tickerEntries = getDailyTickerDataBetweenDates(sp500, startDate, endDate)
    pickleFile(tickerYTDFile, tickerEntries)


def main():
    nArgs = len(sys.argv)
    if nArgs < 2:
        print(
            "\nMust supply at least one argument.\nValid Usage Examples:\n   >> python3 getStockData.py f\n   >> "
            "python3 getStockData.py a\n   >> python3 getStockData.py fa\n "
            "Parameter Info:\nf : fetches stock data from network. Saves to local file\na : adds local data to SQL "
            "database\nfa: does f and a command sequentially\n")
        return
    if sys.argv[1] == 'a' and nArgs == 3:
        print("\nadding local data to SQL database")
        print(sys.argv[2])
        rootPath = sys.argv[2]
        doA(rootPath)
        return
    if sys.argv[1] == 'a' and nArgs == 2:
        print("you must also pass in the current directory. Example getStockdata.py a User/Projects/Stockhub/...")
        print("Setup.sh runs this file automatically.")
        return
    if sys.argv[1] == 'f' and nArgs == 2:
        print("\nOnly do this if you need to! fetching stock data from APIs. This will take ~20minutes due to API "
              "usage constraints.")
        doF()
        return
    if sys.argv[1] == 'fa' and nArgs == 2:
        print("fetch then add to sql database")
        doF()
        doA()
        return


main()
