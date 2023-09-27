import logging

from fastapi import APIRouter, Request
from portfoliotracker.entities import User

from portfoliotracker.repo.db import get_db_connection

from portfoliotracker.repo import TransactionRepo
from portfoliotracker.repo.company_repo import CompanyRepo

from portfoliotracker.service.transaction_service import TransactionService
from portfoliotracker.service.company_service import CompanyService

router = APIRouter()

logger = logging.getLogger(__name__)

db = get_db_connection()


trans_repo = TransactionRepo(db)
trans_service = TransactionService(trans_repo=trans_repo)

company_repo = CompanyRepo(db)
company_service = CompanyService(company_repo=company_repo)


@router.get("/get_sector_stats")
def get_sector_stats(request: Request):

    user = User(username = request.session["username"], user_id = request.session['user_id'])
    holdings = trans_service.get_holdings(trans_service.get_joined_result(user).result)
    sector_summary = trans_service.get_sector_summary(holdings, company_service.get_all_sectors().result)
    instrument_summary = trans_service.get_instrument_summary(holdings, company_service.get_all_instrument().result)
    return{"result": trans_service.sectorDicttoArray(sector_summary)}

