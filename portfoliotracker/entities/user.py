"""
-- Created by: Ashok Kumar Pant
-- Created on: 7/18/23
"""
from pydantic import BaseModel


class User(BaseModel):
    user_id: int = None
    username: str = None
    email: str = None
    password: str = None  # Only for signup
    name: str = None
