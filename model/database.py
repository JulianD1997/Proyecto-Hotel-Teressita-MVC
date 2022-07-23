import sqlite3
import traceback
"""modelo de la base de datos"""
class Database :

    def __init__(self,db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_table(self,query):
        try:
            self.cursor.execute(query)
        except Exception:
            traceback.print_exc()
        finally:
            self.connection.commit()

    def create(self,query,parameters=()):
        try:
            self.cursor.execute(query, parameters)
        except Exception:
            traceback.print_exc()
        finally:
            self.connection.commit()

    def read(self,query,parameters=()):
        try:
            self.cursor.execute(query, parameters)
            return self.cursor.fetchall()
        except Exception:
            traceback.print_exc()
            return False
        finally:
            self.connection.commit()

    def update(self,query,parameters=()):
        try:
            self.cursor.execute(query, parameters)
        except Exception:
            traceback.print_exc()
        finally:
            self.connection.commit()

    def delete(self,query,parameters=()):
        try:
            self.cursor.execute(query, parameters)
        except Exception:
            traceback.print_exc()
        finally:
            self.connection.commit()