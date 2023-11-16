
import logging

from fastapi import APIRouter, Request
from portfoliotracker.repo.db import get_db_connection
from fastapi.templating import Jinja2Templates
from portfoliotracker.entities.user import User

from portfoliotracker.utils.utils import get_templates_directory, check_fileUploaded
from portfoliotracker.service.stock_service import StockService
from portfoliotracker.repo.stock_repo import StockRepo

from fastapi import Request

router = APIRouter()

logger = logging.getLogger(__name__)

db = get_db_connection()
stock_repo = StockRepo(db)
stock_service = StockService(stock_repo=stock_repo)

templates = Jinja2Templates(directory=get_templates_directory())


@router.get("/stock-prices")
def today_prices(request: Request):
    if not request.session["token"]:
        return  templates.TemplateResponse("login.html", { "request": request, "msg":"Please login to continue!"})
    user = User(username = request.session["username"], user_id = request.session['user_id'])
    all_stock = stock_service.get_all_stock_prices()
    trade_date = all_stock.result[0]['trade_date']
    return templates.TemplateResponse("stock.html", {"request": request, "stock_prices": all_stock.result, "trade_date": trade_date, "username": user.username})