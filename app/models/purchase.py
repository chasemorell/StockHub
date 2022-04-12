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
        SELECT id, uid, ticker,num_shares,cost, time_purchased
        FROM Purchases
        WHERE uid = :uid
        ''',
        uid=uid)
        return [Purchase(*row) for row in rows] if rows else None

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

