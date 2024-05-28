from db_connect import Dababase
import logging

class CRUD(Dababase):
    def updateDB(self, table, column, data, exhibit_id):
        sql = f"UPDATE {table} SET {column}='{data}' WHERE exhibit_id = '{exhibit_id}'"
        try:
            self.cursor.execute(sql)
            self.db.commit()
            logging.info("[updateDB] 성공")
        except Exception as e:
            logging.error("[updateDB] 실패", e)