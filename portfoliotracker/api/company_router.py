
import logging
import os
from fastapi.responses import RedirectResponse

from fastapi import APIRouter, Request, Form
from portfoliotracker.repo.db import get_db_connection
from fastapi.templating import Jinja2Templates
from portfoliotracker.entities.company import Company

from portfoliotracker.utils.settings import Settings
from portfoliotracker.utils.utils import get_templates_directory, check_fileUploaded
from portfoliotracker.service.company_service import CompanyService
from portfoliotracker.repo.company_repo import CompanyRepo
from portfoliotracker.repo import TransactionRepo
from portfoliotracker.service.transaction_service import TransactionService
from portfoliotracker.entities import BaseResponse, User
from fastapi import Request

router = APIRouter()

logger = logging.getLogger(__name__)

db = get_db_connection()
company_repo = CompanyRepo(db)
company_service = CompanyService(company_repo=company_repo)

trans_repo = TransactionRepo(db)
trans_service = TransactionService(trans_repo=trans_repo)
templates = Jinja2Templates(directory=get_templates_directory())

@router.get("/companies")
def getCompany(request: Request):
    if not request.session["token"]:
        return  templates.TemplateResponse("login.html", { "request": request, "msg":"Please login to continue!"})
    
    user = User(username = request.session["username"], user_id = request.session['user_id'])
    limit_company = company_service.get_company_info_limit(limit=600)
    return templates.TemplateResponse("companies.html", {"request": request, "limit_company": limit_company.result, "username": user.username})

@router.post("/search_company")
def search_company(company: Company):
    script = company.scrip + "%"
    print(script)
    result = company_service.company_like(script)
    return {"companyList": result.result}

@router.get("/company/{scrip}")
def get_company(scrip, request:Request):
    if not request.session["token"]:
        return  templates.TemplateResponse("login.html", { "request": request, "msg":"Please login to continue!"})
    
    user = User(username = request.session["username"], user_id = request.session['user_id'])
    scrip_transactions = trans_service.get_all_transactions_by_scrip(user, scrip)
    company_transaction_stats = trans_service.company_transaction_stats(user, scrip)
    company_info = company_service.get_company_info(scrip)

    return  templates.TemplateResponse("company.html", {"request": request, "username": user.username, "scrip_transactions":scrip_transactions.result, "company_info":company_info.result, "stats":company_transaction_stats})
