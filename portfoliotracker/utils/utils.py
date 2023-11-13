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
        





