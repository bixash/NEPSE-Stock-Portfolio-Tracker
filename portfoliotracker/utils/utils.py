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
        



def tuple_into_dict(tupe)-> list:
    # tupe = [(39, 'MKHC', '2023-03-17', 10, 0, 10, 'IPO-MKHCL-079/80', 8, 'Maya Khola Hydropower Company Limited', 217.5, '2023-08-13', 215.8)]
    parentDict = []
    for item in tupe:
        dic= dict( tid = item[0], stockSymbol = item[1], transaction_date = item[2], credit_quantity = item[3], debit_quantity = item[4], balance= item[5], desc= item[6], uid= item[7], companyName = item[8], previous_closing= item[9], tradeDate=item[10], closing_price= item[11] )
        parentDict.append(dic)
    return parentDict


