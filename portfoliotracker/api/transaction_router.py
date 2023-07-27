"""
-- Created by: Ashok Kumar Pant
-- Created on: 7/18/23
"""

import logging

from fastapi import APIRouter, Request
from portfoliotracker.repo.db import get_db_connection
from portfoliotracker.repo.transaction_repo import TransactionRepo
from portfoliotracker.service.transaction_service import TransactionService
from portfoliotracker.entities import Transaction
from fastapi.templating import Jinja2Templates
from portfoliotracker.utils import Settings, get_templates_directory

router = APIRouter()

logger = logging.getLogger(__name__)

db = get_db_connection()
transaction_repo = TransactionRepo(db)
transaction_service = TransactionService(trans_repo=transaction_repo)
templates = Jinja2Templates(directory=get_templates_directory())

@router.get("/transaction")
def get_transaction(request: Request):
    if not request.session["token"]:
        return templates.TemplateResponse("login.html", { "request": request, "msg":"Please login to continue!"})
    token = request.session["token"]
    user_id = request.session['user_id']

    
    return 
    