"""
-- Created by: Ashok Kumar Pant
-- Created on: 7/18/23
"""
import logging

from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse


from portfoliotracker.entities import BaseResponse, User
from portfoliotracker.entities.auth import LoginRequest
from portfoliotracker.repo.auth_repo import AuthRepo
from portfoliotracker.repo.db import get_db_connection
from portfoliotracker.service.auth_service import AuthService
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

router = APIRouter()

logger = logging.getLogger(__name__)

db = get_db_connection()
auth_repo = AuthRepo(db)
auth_service = AuthService(auth_repo=auth_repo)



templates_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "resources", "templates")
templates = Jinja2Templates(directory=templates_directory)


@router.get('/auth/login')
def get_login(request: Request):
    return templates.TemplateResponse("login.html",{ "request": request})

@router.post('/auth/login')
def post_login(login_request: LoginRequest, request: Request):
   
    response = auth_service.login(login_request.email, login_request.password)
        
    if response.error:
        return templates.TemplateResponse("login.html",{ "request": request, "msg": response.msg})
    
    request.session["token"] = response.result.token
    request.session["username"] = response.result.user.username

    return templates.TemplateResponse("dashboard.html",{ "request": request, "username": request.session["username"]})

@router.post('/auth/signup')
def signup(user: User) -> BaseResponse:
    return auth_service.signup(user)


@router.post('/auth/logout')
def logout(request: Request):
    token = request.session["token"]
    auth_service.logout(token)
