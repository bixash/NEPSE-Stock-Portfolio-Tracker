"""
-- Created by: Ashok Kumar Pant
-- Created on: 7/18/23
"""
import logging

from fastapi import APIRouter

from portfoliotracker.entities import BaseResponse, User
from portfoliotracker.entities.auth import LoginRequest
from portfoliotracker.repo.auth_repo import AuthRepo
from portfoliotracker.repo.db import get_db_connection
from portfoliotracker.service.auth_service import AuthService

router = APIRouter()

logger = logging.getLogger(__name__)

db = get_db_connection()
auth_repo = AuthRepo(db)
auth_service = AuthService(auth_repo=auth_repo)


@router.post('/auth/login')
def login(login_request: LoginRequest) -> BaseResponse:
    # Set session
    return auth_service.login(login_request.email, login_request.password)


@router.post('/auth/signup')
def signup(user: User) -> BaseResponse:
    return auth_service.signup(user)


@router.post('/auth/logout')
def logout():
    token = None
    auth_service.logout(token)
