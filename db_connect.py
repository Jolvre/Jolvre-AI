import psycopg2
import logging

class Dababase():
    def __init__(self, host, dbname, user, passwd, port) -> None:
        self.db = psycopg2.connect(host=host, dbname=dbname, user=user, password=passwd, port=port)
        self.cursor = self.db.cursor()
    
    # DB Connect Close
    def __del__(self):
        self.db.close()
        self.cursor.close()
    
    def execute(self, query, **kwargs):
        self.cursor.execute(query=query)
        row = self.cursor.fetchall()
        return row
    
    def commit(self):
        self.cursor.commit()
    
