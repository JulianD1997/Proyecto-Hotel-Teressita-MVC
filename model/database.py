import sqlite3
import traceback

class Database():
    def __init__(self,db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
      
    def action(self,query,parameters=()):
        try:
            self.cursor.execute(query, parameters)
            return self.cursor.fetchall()
        except Exception:
            traceback.print_exc()
            return False
        finally:
            self.connection.commit()