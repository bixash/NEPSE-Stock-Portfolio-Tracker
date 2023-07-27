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

router = APIRouter()

logger = logging.getLogger(__name__)

db = get_db_connection()
transaction_repo = TransactionRepo(db)
transaction_service = TransactionService(trans_repo=transaction_repo)

@router.get("/transaction")
def get_transaction(request: Request):
    token = request.session["token"]
    user_id = request.session['user_id']

    
    return 
    