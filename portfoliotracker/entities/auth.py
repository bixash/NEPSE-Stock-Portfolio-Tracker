"""
-- Created by: Ashok Kumar Pant
-- Created on: 7/18/23
"""
from pydantic import BaseModel

from portfoliotracker.entities.user import User


class LoginRequest(BaseModel):
    email: str = None
    password: str = None


class AuthResponse(BaseModel):
    token: str = None
    user: User = None

class SignupRequest(BaseModel):
    username: str = None
    email: str = None
    password: str = None
