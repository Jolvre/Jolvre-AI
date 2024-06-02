import pymysql
import logging

class Database():
    def __init__(self, host, dbname, user, passwd, port) -> None:
        self.db = pymysql.connect(host=host, database=dbname, user=user, password=passwd, port=port)
        self.cursor = self.db.cursor()
    
    # DB Connect Close
    def __del__(self):
        self.db.close()
    
    def execute(self, query, **kwargs):
        self.cursor.execute(query, **kwargs)
        rows = self.cursor.fetchall()
        return rows
    
    def commit(self):
        self.db.commit()