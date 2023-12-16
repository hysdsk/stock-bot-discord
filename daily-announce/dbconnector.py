from mysql import connector as mc


class Connector(object):
    def __init__(self, hostname, username, password, dbname):
        self.host = hostname
        self.user = username
        self.pswd = password
        self.name = dbname

    def find(self, sql, params=None):
        with mc.connect(host=self.host, user=self.user, password=self.pswd, database=self.name) as connection:
            cursor = connection.cursor()
            cursor.execute(sql, params)
            return cursor.fetchall()

    def save(self, sql, params):
        with mc.connect(host=self.host, user=self.user, password=self.pswd, database=self.name) as connection:
            cursor = connection.cursor()
            cursor.execute(sql, params)
            cursor.close()
            connection.commit()


class KabuConnector(Connector):
    def __init__(self, hostname, username, password):
        super().__init__(hostname, username, password, "kabu")

    def find_by_symbol(self, code: str):
        sql = """
            SELECT
                code
            FROM
                symbols
            WHERE
                code = %s
        """
        rows = super().find(sql, params=(code,))
        return [{
            "code": row[0],
        } for row in rows]

    def save_one(self, code: str):
        sql = """
            INSERT INTO symbols (code) VALUES (%s);
        """
        super().save(sql, params=(code,))
