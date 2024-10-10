
import logging

from fastapi import APIRouter, Request
from portfoliotracker.repo.db import get_db_connection
from fastapi.templating import Jinja2Templates
from portfoliotracker.entities.company import Company
from portfoliotracker.repo.stock_repo import StockRepo
from portfoliotracker.service.stock_service import StockService

from portfoliotracker.utils.utils import get_templates_directory
from portfoliotracker.service.company_service import CompanyService
from portfoliotracker.repo.company_repo import CompanyRepo
from portfoliotracker.repo import TransactionRepo
from portfoliotracker.service.transaction_service import TransactionService
from portfoliotracker.entities import User
from fastapi import Request

router = APIRouter()

logger = logging.getLogger(__name__)

db = get_db_connection()
company_repo = CompanyRepo(db)
company_service = CompanyService(company_repo=company_repo)

trans_repo = TransactionRepo(db)
trans_service = TransactionService(trans_repo=trans_repo)

stock_repo= StockRepo(db)
stock_service = StockService(stock_repo=stock_repo)

templates = Jinja2Templates(directory=get_templates_directory())

@router.get("/company/all")
def getCompany(request: Request):
    if not request.session:
        return  templates.TemplateResponse("login.html", { "request": request, "msg":"Please login to continue!"})
    
    user = User(username = request.session["username"], user_id = request.session['user_id'])
    
    if not company_repo.retrieve_companyInfo_all_limit(limit=1):
        company_service.upload_company_csv()
    limit_company = company_service.get_company_info_limit(limit=600)
    return templates.TemplateResponse("companies.html", {"request": request, "limit_company": limit_company.result, "username": user.username})
 
        

@router.post("/company/search")
def search_company(company: Company):
    if not company_repo.retrieve_companyInfo_all_limit(limit=1):
        company_service.upload_company_csv()
    script = company.scrip + "%"
    result = company_service.company_like(script)
    return {"companyList": result.result}

@router.get("/company/{scrip}")
def get_company(scrip, request:Request):
    if not request.session["token"]:
        return  templates.TemplateResponse("login.html", { "request": request, "msg":"Please login to continue!"})
    
    user = User(username = request.session["username"], user_id = request.session['user_id'])
    if not company_repo.retrieve_companyInfo_all_limit(limit=1):
        company_service.upload_company_csv()
    company_transactions = trans_service.get_all_transactions_by_scrip(user, scrip)
    company_stats = trans_service.stock_transaction_stats(user, scrip)
    company_info = company_service.get_company_info(scrip)
    stock_info = stock_service.get_stock_by_scrip(scrip).result


    return  templates.TemplateResponse("company.html", {"request": request, "username": user.username, "scrip_transactions":company_transactions.result, "company_info":company_info.result, "stats":company_stats, "stock_info": stock_info})
