from flask import current_app as app


class Purchase:
    def __init__(self, id, uid, pid, time_purchased):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.time_purchased = time_purchased

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
        SELECT id, uid, ticker, time_purchased
        FROM Purchases
        WHERE uid = :uid
        ''',
        id=id)
        return [Purchase(*row) for row in rows] if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
            SELECT id, uid, ticker, time_purchased
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
        rows = app.db.execute(f'SELECT id, uid, ticker, time_purchased FROM Purchases WHERE uid = {uid} ORDER BY {sort}')

        return [Purchase(*row) for row in rows] if rows else []

    @staticmethod
    def get_by_search(uid, searchInput):
        sqlSearchInput = '%' + searchInput + '%'
        rows = app.db.execute('''
        SELECT id, uid, ticker, time_purchased
        FROM Purchases
        WHERE ticker ILIKE :s AND uid = :uid
        ORDER BY time_purchased DESC ''', s=sqlSearchInput, uid=uid)

        return [Purchase(*row) for row in rows] if rows else []

