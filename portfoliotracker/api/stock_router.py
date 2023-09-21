
import logging

from fastapi import APIRouter, Request
from portfoliotracker.repo.db import get_db_connection
from fastapi.templating import Jinja2Templates
from portfoliotracker.entities.stock import Stock

from portfoliotracker.utils.utils import get_templates_directory, check_fileUploaded
from portfoliotracker.service.api_service import APIService
from portfoliotracker.repo.api_repo import APIRepo

from fastapi import Request

router = APIRouter()

logger = logging.getLogger(__name__)

db = get_db_connection()
api_repo = APIRepo(db)
api_service = APIService(api_repo=api_repo)

templates = Jinja2Templates(directory=get_templates_directory())


@router.get("/stock-prices")
def today_prices(request: Request):
    if not request.session["token"]:
        return  templates.TemplateResponse("login.html", { "request": request, "msg":"Please login to continue!"})
    all_stock = api_service.get_all_stock_prices()
    return templates.TemplateResponse("stock.html", {"request": request, "stock_prices": all_stock.result})