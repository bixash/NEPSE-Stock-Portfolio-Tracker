"""
-- Created by: Ashok Kumar Pant
-- Created on: 7/18/23
"""

import logging

from fastapi import APIRouter, Request
from portfoliotracker.repo.db import get_db_connection
from portfoliotracker.repo.transaction_repo import TransactionRepo
from portfoliotracker.service.transaction_service import TransactionService
from portfoliotracker.entities import Transaction, User
from fastapi.templating import Jinja2Templates
from portfoliotracker.utils import Settings, get_templates_directory

router = APIRouter()

logger = logging.getLogger(__name__)

db = get_db_connection()
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
    