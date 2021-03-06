from flask import current_app as app


class Purchase:
    def __init__(self, id, uid, ticker,num_shares, cost, time_purchased):
        self.id = id
        self.uid = uid
        self.ticker = ticker
        self.num_shares=num_shares
        self.cost=cost
        self.time_purchased = time_purchased

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
        SELECT id, uid, ticker, num_shares, cost, time_purchased
        FROM Purchases
        WHERE uid = :uid
        ''',
        uid=uid)
        return [Purchase(*row) for row in rows] if rows else []

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
            SELECT  id, uid, ticker,num_shares,cost, time_purchased
            FROM Purchases
            WHERE uid = :uid
            AND time_purchased >= :since
            ORDER BY time_purchased DESC
            ''',
              uid=uid,
              since=since)
        return [Purchase(*row) for row in rows] if rows else [] #This is a quick fix (the [] instead of None)

    @staticmethod
    def get_all_by_uid(uid, sort = 'time_purchased DESC'):
        rows = app.db.execute(f'SELECT id, uid, ticker, num_shares, cost,time_purchased FROM Purchases WHERE uid = {uid} ORDER BY {sort}')

        return [Purchase(*row) for row in rows] if rows else    []

    @staticmethod
    def get_by_search(uid, searchInput):
        sqlSearchInput = '%' + searchInput + '%'
        rows = app.db.execute('''
        SELECT id, uid, ticker, time_purchased, num_shares, cost
        FROM Purchases
        WHERE ticker ILIKE :s AND uid = :uid
        ORDER BY time_purchased DESC ''', s=sqlSearchInput, uid=uid)

        return [Purchase(*row) for row in rows] if rows else []

    @staticmethod
    def get_user_portfolio(uid):
        rows = app.db.execute('''
            SELECT uid, ticker, SUM(num_shares) AS sum_shares , SUM(cost) AS sum_cost
            FROM Purchases
            WHERE uid = :uid
            GROUP BY uid, ticker HAVING SUM(cost) <> 0
            ORDER BY ticker DESC
            ''',
              uid=uid,)
        return rows if rows else [] #This is a quick fix (the [] instead of None)

    @staticmethod
    def get_shares_quantity_money_val(uid, ticker):
        rows = app.db.execute('''
        SELECT ticker, SUM(num_shares) AS sum_shares , SUM(cost) AS sum_cost
        FROM Purchases
        WHERE uid = :uid AND ticker=:ticker
        GROUP BY ticker
         ''', ticker=ticker, uid=uid)

        return rows if rows else []
