"""
-- Created by: Ashok Kumar Pant
-- Created on: 7/18/23
"""
import logging

from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse


from portfoliotracker.entities import BaseResponse, User
from portfoliotracker.entities.auth import LoginRequest, SignupRequest
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
def login(request: Request):
    return templates.TemplateResponse("login.html",{ "request": request})

@router.post('/auth/login')
def login(request: Request, email: str = Form(), password: str = Form()):

    login_request = LoginRequest(email=email, password=password)
   
    response = auth_service.login(login_request.email, login_request.password)
        
    if response.error:
        return templates.TemplateResponse("login.html",{ "request": request, "msg": response.msg})
    
    request.session["token"] = response.result.token
    request.session["username"] = response.result.user.username
    request.session['user_id'] = response.result.user.user_id

    return RedirectResponse(url=request.url_for("portfolio"), status_code=status.HTTP_303_SEE_OTHER)

@router.get('/auth/signup')
def signup(request: Request):
    return templates.TemplateResponse("signup.html",{ "request": request})

@router.post('/auth/signup')
def signup(request: Request, username: str = Form(), email: str = Form(), password: str = Form()):

    signup_request = SignupRequest(username=username, email=email, password=password)

    response = auth_service.signup(signup_request)
    if response.error:
        return templates.TemplateResponse("signup.html",{ "request": request, "msg": response.msg})
    return templates.TemplateResponse("login.html",{ "request": request, "msg": "Registered successful!"})

@router.get('/auth/logout')
def logout(request: Request):
    token = request.session["token"]
    auth_service.logout(token)
    request.session["token"] = None
    return RedirectResponse(url=request.url_for("root"), status_code=status.HTTP_303_SEE_OTHER)
