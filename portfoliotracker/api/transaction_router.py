"""
-- Created by: Ashok Kumar Pant
-- Created on: 7/18/23
"""

import logging
from portfoliotracker.repo.user_repo import UserRepo
from portfoliotracker.service.user_service import UserService
from fastapi import APIRouter, Request, Form
from portfoliotracker.repo.db import get_db_connection
from portfoliotracker.repo.transaction_repo import TransactionRepo
from portfoliotracker.service.transaction_service import TransactionService
from portfoliotracker.entities import Transaction, User
from fastapi.templating import Jinja2Templates
from portfoliotracker.utils import Settings, get_templates_directory

router = APIRouter()

logger = logging.getLogger(__name__)

db = get_db_connection()
user_repo = UserRepo(db)
user_service = UserService(user_repo=user_repo)
trans_repo = TransactionRepo(db)
trans_service = TransactionService(trans_repo=trans_repo)
templates = Jinja2Templates(directory=get_templates_directory())

@router.get("/transactions")
def get_transaction(request: Request):
    if not request.session["token"]:
        return templates.TemplateResponse("login.html", { "request": request, "msg":"Please login to continue!"})
    token = request.session["token"]
    user_id = request.session['user_id']
    user = User(username = request.session["username"], user_id = request.session['user_id'])

    all_transactions = trans_service.all_transactions(user).result
    # print(all_transactions)
    
    return templates.TemplateResponse("history.html", { "request": request, "username": user.username, "all_transactions": all_transactions})

@router.post('/transactions/delete-data')
def delete_data(request: Request, password: str = Form()):
    if not request.session["token"]:
        return  templates.TemplateResponse("login.html", { "request": request, "msg":"Please login to continue!"})
    
    user = User(username = request.session["username"], user_id = request.session['user_id'])

    response = user_service.get_user(user.user_id).result
    real_pass = response.password
    typed_pass = password

    if real_pass == typed_pass:
        if trans_service.delete_transactions(user.user_id).success:
            return templates.TemplateResponse("profile.html", { "request": request,  "user_id": user.user_id, "username": user.username, "email": response.email, "msg": "Your transactions data was deleted permanently!"})
    else:
        return templates.TemplateResponse("profile.html", { "request": request,  "user_id": user.user_id, "username": user.username, "email": response.email, "msg": "Sorry password invalid!"})