"""
-- Created by: Ashok Kumar Pant
-- Created on: 7/18/23
"""
from portfoliotracker.entities import User
from portfoliotracker.repo.db import DBConnection


class AuthRepo:
    def __init__(self, db: DBConnection):
        self.db = db

    def get_user_by_email(self, email: str) -> User:
        cur = self.db.get_connection()
        cur.execute("SELECT id, username, email FROM `user` where email= ?", (email, ))
        result = cur.fetchone()
        if result:
            return User(user_id=result[0], username=result[1], email=result[2])
        return None

    def login(self, email: str, password: str) -> bool:
        cur = self.db.get_connection()
        cur.execute("SELECT id, username FROM `user` where email= ? and password = ?", (email, password, ))
        result = cur.fetchone()
        if result:
            return True
        return False

    def save_user(self, signup_user) -> bool:
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("INSERT INTO `user` (username, email, password) VALUES (?, ?, ?)", (signup_user.username, signup_user.email, signup_user.password, ))
        con.commit()
        return True
