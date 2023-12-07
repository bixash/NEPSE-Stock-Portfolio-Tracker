import abc
import sqlite3 as sql
import traceback
from typing import Optional

from portfoliotracker.utils.settings import Settings


class DBConnection(abc.ABC):
    def __init__(self):
        self.con = sql.connect(Settings.SQLITE_DB_PATH, check_same_thread=False)
        self.cur = self.con.cursor()

    def get_connection(self):
        return self.con
    
    def get_cursor(self):
        return self.cur
        

    def commit(self):
        self.con.commit()

    def close(self):
        self.con.close()
        

    def __exit__(self):
        self.con.commit()
        self.con.close()


DB_CONNECTION: Optional[DBConnection] = None


def _build_db_connection() -> DBConnection:
    global DB_CONNECTION
    try:
        DB_CONNECTION = DBConnection()
    except Exception as e:
        traceback.print_exc()


def get_db_connection() -> DBConnection:
    if DB_CONNECTION is None:
        _build_db_connection()
    return DB_CONNECTION
