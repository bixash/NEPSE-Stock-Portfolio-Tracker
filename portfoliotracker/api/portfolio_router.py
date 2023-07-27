"""
-- Created by: Ashok Kumar Pant
-- Created on: 7/18/23
"""
import logging

from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse


from portfoliotracker.entities import BaseResponse, User
from portfoliotracker.entities.auth import LoginRequest, SignupRequest

from portfoliotracker.repo import TransactionRepo
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
trans_repo = TransactionRepo(db)



templates_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "resources", "templates")
templates = Jinja2Templates(directory=templates_directory)

@router.get('/portfolio', name ="portfolio")
def portfolio(request: Request):
    if not request.session["token"]:
        return  templates.TemplateResponse("login.html", { "request": request, "msg":"Please login to continue!"})
    user = User(username = request.session["username"], user_id = request.session['user_id'])
    all_history = trans_repo.retrieve_all_transaction(user)

    return templates.TemplateResponse("portfolio.html", { "request": request, "transaction": all_history, "username": user.username})

