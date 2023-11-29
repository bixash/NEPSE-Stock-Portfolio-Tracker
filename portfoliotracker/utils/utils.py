"""
-- Created by: Ashok Kumar Pant
-- Created on: 7/18/23
"""


def generate_uuid():
    import uuid
    return str(uuid.uuid4())


def get_templates_directory():
    import os.path
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "resources", "templates")

def check_valid_user()-> bool:
    from fastapi import Request 
    if Request.session["token"] is None:
        return False
    else:
        return True

def check_fileUploaded(file_location: str, file)->bool:
    try:
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
            return True
    except Exception:
        return False
    finally:
        file.file.close()
        

def validate_email(email:str)-> bool:
    import re
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, email):
        return True
    return False
    
def check_password(user_id:int, typed_password:str)->bool:
    from portfoliotracker.repo.db import get_db_connection
    from portfoliotracker.repo.user_repo import UserRepo
    user_repo = UserRepo(get_db_connection())
    if user_repo.get_user_password(user_id):
        real_password = user_repo.get_user_password(user_id)
        if real_password == typed_password:
            return True
    return False


def dictifiy_transactions(transactions:tuple):
        from portfoliotracker.utils.methods import convert_date_format
        # MKHC|2023-03-17|10|0|10|IPO-MKHCL-079/80|100.0|1
        resultList = []
        for item in transactions:
            transaction = dict(scrip = item[0], transaction_date= convert_date_format(item[1]), credit_quantity = item[2], debit_quantity = item[3], after_balance = item[4], history_description =item[5], unit_price =item[6],tid = item[7])
            resultList.append(transaction)
        return resultList