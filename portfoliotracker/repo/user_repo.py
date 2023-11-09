from portfoliotracker.entities import User
from portfoliotracker.repo.db import DBConnection


class UserRepo:
    def __init__(self, db: DBConnection):
        self.db = db

    def get_user_by_id(self, user_id: int) -> User:
        cur = self.db.get_connection()
        cur.execute("SELECT username, email, password FROM `user` where id = ?", (user_id, ))
        result = cur.fetchone()
        if result:
            return User(username=result[0], email=result[1], password=result[2])
        return None

    def update_user_by_id(self, user:User) -> bool:
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("UPDATE `user` set username = ?, email = ?, password = ? WHERE id = ? ", (user.username, user.email, user.password, user.user_id,  ))
        con.commit()
        return True
    
    def update_user_username(self, username:str, user_id:int) -> bool:
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("UPDATE `user` set username = ? WHERE id = ? ", (username, user_id,))
        con.commit()
        return True
    
    def update_user_password(self, password:str, user_id:int) -> bool:
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("UPDATE `user` set password = ? WHERE id = ? ", (password, user_id, ))
        con.commit()
        return True

    def update_user_email(self, email:str, user_id:int) -> bool:
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("UPDATE `user` set email = ? WHERE id = ? ", (email, user_id,  ))
        con.commit()
        return True
    

    def delete_user(self, user_id:int) -> bool:
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("DELETE FROM `user` WHERE id = ? ", ( user_id,  ))
        con.commit()
        return True