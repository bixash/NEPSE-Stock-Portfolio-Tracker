
import logging
import os
from fastapi.responses import RedirectResponse

from fastapi import APIRouter, Request
from portfoliotracker.repo.db import get_db_connection
from fastapi.templating import Jinja2Templates
from portfoliotracker.entities.company import Company

from portfoliotracker.utils.settings import Settings
from portfoliotracker.utils.utils import get_templates_directory, check_fileUploaded
from portfoliotracker.service.company_service import CompanyService
from portfoliotracker.repo.company_repo import CompanyRepo

from fastapi import Request

router = APIRouter()

logger = logging.getLogger(__name__)

db = get_db_connection()
company_repo = CompanyRepo(db)
company_service = CompanyService(company_repo=company_repo)

templates = Jinja2Templates(directory=get_templates_directory())

@router.get("/company")
def getCompany(request: Request):
    if not request.session["token"]:
        return  templates.TemplateResponse("login.html", { "request": request, "msg":"Please login to continue!"})
    
    limit_company = company_service.get_company_info_limit(limit=20)
    return templates.TemplateResponse("company.html", {"request": request, "limit_company": limit_company.result})




@router.post("/get_company")
def search_company(company: Company):
    script = company.scrip + "%"
    result = company_service.company_like(script)
    print(result.result)
    return {"message": result.result}