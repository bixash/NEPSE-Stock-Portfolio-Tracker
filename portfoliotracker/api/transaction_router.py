"""
-- Created by: Ashok Kumar Pant
-- Created on: 7/18/23
"""

import logging
import os
from fastapi.responses import RedirectResponse

from fastapi import APIRouter, Request, Form,  UploadFile, status
from portfoliotracker.repo.db import get_db_connection

from portfoliotracker.utils.utils import get_templates_directory, check_fileUploaded
from portfoliotracker.repo.user_repo import UserRepo
from portfoliotracker.service.user_service import UserService
from portfoliotracker.repo.transaction_repo import TransactionRepo
from portfoliotracker.service.transaction_service import TransactionService
from portfoliotracker.repo.company_repo import CompanyRepo
from portfoliotracker.service.company_service import CompanyService

from portfoliotracker.entities import User

from fastapi.templating import Jinja2Templates
from portfoliotracker.utils import Settings, get_templates_directory

router = APIRouter()

logger = logging.getLogger(__name__)

db = get_db_connection()
user_repo = UserRepo(db)
user_service = UserService(user_repo=user_repo)
trans_repo = TransactionRepo(db)
trans_service = TransactionService(trans_repo=trans_repo)

company_repo = CompanyRepo(db)
company_service = CompanyService(company_repo=company_repo)

templates = Jinja2Templates(directory=get_templates_directory())

@router.get("/transactions")
def get_transaction(request: Request):
    if not request.session["token"]:
        return templates.TemplateResponse("login.html", { "request": request, "msg":"Please login to continue!"})
    token = request.session["token"]
    user_id = request.session['user_id']
    user = User(username = request.session["username"], user_id = request.session['user_id'])

    all_transactions = trans_service.all_transactions(user).result
    # print(all_transactions)
    
    return templates.TemplateResponse("history.html", { "request": request, "username": user.username, "all_transactions": all_transactions})


@router.get("/transactions/holdings")
def holdings(request: Request):
    if not request.session["token"]:
        return templates.TemplateResponse("login.html", { "request": request, "msg":"Please login to continue!"})
    token = request.session["token"]
    user_id = request.session['user_id']


    user = User(username = request.session["username"], user_id = request.session['user_id'])

    if trans_service.holdings_stats(user):
        holdings = trans_service.holdings_only(user)
        holdings_summary = trans_service.holdings_summary(trans_service.holdings_only(user))

        return templates.TemplateResponse("holdings.html", { "request": request, "username": user.username, "holdings": holdings, 'holdings_summary': holdings_summary,})

    return templates.TemplateResponse("holdings.html", { "request": request,  "username": user.username, "holdings": []})

@router.get("/transactions/upload")
def upload(request: Request):
    if not request.session["token"]:
        return  templates.TemplateResponse("login.html", { "request": request, "msg":"Please login to continue!"})
    user = User(username = request.session["username"], user_id = request.session['user_id'])
    return templates.TemplateResponse("upload.html", {"request": request, "username": user.username})


@router.post("/transactions/upload")
def upload(request: Request, file: UploadFile):
    user = User(username = request.session["username"], user_id = request.session['user_id'])

    filename = file.filename
    file_location = f"{os.path.join(Settings.CSV_UPLOAD_PATH)}/{user.user_id}_{user.username}_transactions.csv"

    if not file:
        return templates.TemplateResponse("upload.html", {"request": request, "username": user.username, "msg": "No upload file sent!"})
    if filename == '':
        return templates.TemplateResponse("upload.html", {"request": request, "username": user.username, "msg": "No file selected!"})
    if not filename.endswith('.csv'):
        return templates.TemplateResponse("upload.html", {"request": request, "username": user.username, "msg": "File should be in .csv extension!"})
    
    if not check_fileUploaded(file_location, file):
        return templates.TemplateResponse("upload.html", {"request": request, "username": user.username, "msg": "File can't be uploaded!"})

    if trans_service.check_user_transactions(user):
        trans_repo.delete_transaction(user.user_id)
        
    response = trans_service.upload_transactions(user, file_location)
    if response.error:
        return templates.TemplateResponse("upload.html",{ "request": request, "msg": response.msg, "username": user.username})
    return RedirectResponse(url=request.url_for("portfolio"), status_code=status.HTTP_303_SEE_OTHER)


@router.post('/transactions/delete-data')
def delete_data(request: Request, password: str = Form()):
    if not request.session["token"]:
        return  templates.TemplateResponse("login.html", { "request": request, "msg":"Please login to continue!"})
    
    user = User(username = request.session["username"], user_id = request.session['user_id'])

    real = user_service.get_user(user.user_id).result

    if real.password == password:
        if trans_service.delete_transactions(user.user_id).success:
            return templates.TemplateResponse("profile.html", { "request": request,  "user_id": user.user_id, "username": user.username, "email": real.email, "msg": "Your transactions data was deleted permanently!"})
    else:
        return templates.TemplateResponse("profile.html", { "request": request,  "user_id": user.user_id, "username": user.username, "email": real.email, "msg": "Sorry password invalid!"})
    
@router.get("/transactions/get_sector_stats")
def get_sector_stats(request: Request):

    user = User(username = request.session["username"], user_id = request.session['user_id'])
    holdings = trans_service.get_holdings(trans_service.get_joined_result(user).result)
    sector_summary = trans_service.get_sector_summary(holdings, company_service.get_all_sectors().result)
    instrument_summary = trans_service.get_instrument_summary(holdings, company_service.get_all_instrument().result)


    return{"result": trans_service.XYarray(sector_summary)}