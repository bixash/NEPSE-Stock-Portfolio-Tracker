
import logging

from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse


from portfoliotracker.entities import BaseResponse, User
from portfoliotracker.entities.auth import LoginRequest, SignupRequest

from portfoliotracker.repo import TransactionRepo
from portfoliotracker.repo.auth_repo import AuthRepo
from portfoliotracker.repo.api_repo import APIRepo
from portfoliotracker.repo.company_repo import CompanyRepo

from portfoliotracker.repo.db import get_db_connection

from portfoliotracker.service.auth_service import AuthService
from portfoliotracker.service.api_service import APIService
from portfoliotracker.service.transaction_service import TransactionService
from portfoliotracker.service.company_service import CompanyService

from portfoliotracker.utils import  tuple_into_dict

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
trans_service = TransactionService(trans_repo=trans_repo)

api_repo = APIRepo(db)
api_service = APIService(api_repo=api_repo)

company_repo = CompanyRepo(db)
company_service = CompanyService(company_repo=company_repo)

templates_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "resources", "templates")
templates = Jinja2Templates(directory=templates_directory)

@router.get('/portfolio', name ="portfolio")
def portfolio(request: Request):
    if not request.session["token"]:
        return  templates.TemplateResponse("login.html", { "request": request, "msg":"Please login to continue!"})
   
    user = User(username = request.session["username"], user_id = request.session['user_id'])

   
    if not api_service.is_tradeDate_same():
        response = api_service.update_prices_todb()
        print(response.msg)

    holdings = trans_service.get_holdings(trans_service.get_joined_result(user).result)
    recent_transactions = trans_service.recent_transactions(user).result
    
    holdings_summary = trans_service.get_holdings_summary(holdings)
    sector_summary = trans_service.get_sector_summary(holdings, company_service.get_all_sectors().result)
    instrument_summary = trans_service.get_instrument_summary(holdings, company_service.get_all_instrument().result)
    # print(holdings_summary)

    return templates.TemplateResponse("portfolio.html", { "request": request,  "recent_transactions": recent_transactions,"username": user.username, "holdings": holdings, "holdings_summary": holdings_summary, "sector_summary":sector_summary, "instrument_summary": instrument_summary })


