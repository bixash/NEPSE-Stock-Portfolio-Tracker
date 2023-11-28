
import logging

from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse


from portfoliotracker.entities import BaseResponse, User
from portfoliotracker.entities.auth import LoginRequest, SignupRequest

from portfoliotracker.repo import TransactionRepo
from portfoliotracker.repo.auth_repo import AuthRepo
from portfoliotracker.repo.stock_repo import StockRepo
from portfoliotracker.repo.company_repo import CompanyRepo

from portfoliotracker.repo.db import get_db_connection

from portfoliotracker.service.auth_service import AuthService
from portfoliotracker.service.stock_service import StockService
from portfoliotracker.service.transaction_service import TransactionService
from portfoliotracker.service.company_service import CompanyService



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

stock_repo = StockRepo(db)
stock_service = StockService(stock_repo=stock_repo)

company_repo = CompanyRepo(db)
company_service = CompanyService(company_repo=company_repo)

templates_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "resources", "templates")
templates = Jinja2Templates(directory=templates_directory)

@router.get('/portfolio', name ="portfolio")
def portfolio(request: Request):
    if not request.session["token"]:
        return  templates.TemplateResponse("login.html", { "request": request, "msg":"Please login to continue!"})
   
    user = User(username = request.session["username"], user_id = request.session['user_id'])

    if stock_service.get_stock_prices_from_api().success:
        if not stock_service.is_tradeDate_same_db():
            stock_service.update_prices_todb()
       

    if trans_service.check_user_transactions(user):
        
        portfolio_summary = trans_service.portfolio_summary(trans_service.holdings_stats(user))
        recent_transactions = trans_service.recent_transactions(user).result
        holdings_summary = trans_service.holdings_summary(trans_service.holdings_only(user))
        
        sector_summary = trans_service.sector_summary(trans_service.company_stats(user))
        instrument_summary = trans_service.instrument_summary(trans_service.company_stats(user))
        holdings_length = len(trans_service.holdings_only(user))
    
        return templates.TemplateResponse("portfolio.html", { "request": request,  "recent_transactions": recent_transactions,"username": user.username, "holdings_summary": holdings_summary,  "portfolio_summary": portfolio_summary, "sector_summary":sector_summary, "instrument_summary": instrument_summary, "holdings_length": holdings_length, "flag":False })
    
    return templates.TemplateResponse("portfolio.html", { "request": request,  "username": user.username, "flag": True})

