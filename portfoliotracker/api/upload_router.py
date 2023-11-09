
import logging
import os
from fastapi.responses import RedirectResponse

from fastapi import APIRouter, Request, UploadFile, status
from portfoliotracker.repo.db import get_db_connection
from fastapi.templating import Jinja2Templates
from portfoliotracker.entities import User

from portfoliotracker.utils.settings import Settings
from portfoliotracker.utils.utils import get_templates_directory, check_fileUploaded
from portfoliotracker.service.transaction_service import TransactionService
from portfoliotracker.repo.transaction_repo import TransactionRepo



router = APIRouter()

logger = logging.getLogger(__name__)

db = get_db_connection()
trans_repo = TransactionRepo(db)
trans_service = TransactionService(trans_repo=trans_repo)

templates = Jinja2Templates(directory=get_templates_directory())


@router.get("/upload")
def upload(request: Request):
    if not request.session["token"]:
        return  templates.TemplateResponse("login.html", { "request": request, "msg":"Please login to continue!"})
    user = User(username = request.session["username"], user_id = request.session['user_id'])
    return templates.TemplateResponse("upload.html", {"request": request, "username": user.username})


@router.post("/upload")
def upload(request: Request, file: UploadFile):
    user = User(username = request.session["username"], user_id = request.session['user_id'])

    filename = file.filename
    file_location = f"{os.path.join(Settings.CSV_UPLOAD_PATH)}/{user.user_id}_{user.username}_transactions.csv"

    if not file:
        return templates.TemplateResponse("upload.html", {"request": request, "username": user.username, "msg": "No upload file sent!"})
    if filename == '':
        return templates.TemplateResponse("upload.html", {"request": request, "username": user.username, "msg": "No file selected!"})
    if not filename.endswith('.csv'):
        return templates.TemplateResponse("upload.html", {"request": request, "username": user.username, "msg": "File should be csv format!"})
    
    if not check_fileUploaded(file_location, file):
        return templates.TemplateResponse("upload.html", {"request": request, "username": user.username, "msg": "File can't be uploaded!"})

    if trans_service.check_transaction(user):
        trans_repo.delete_transaction(user.user_id)
        
    response = trans_service.upload_transactions(user, file_location)
    if response.error:
        return templates.TemplateResponse("upload.html",{ "request": request, "msg": response.msg, "username": user.username})
    return RedirectResponse(url=request.url_for("portfolio"), status_code=status.HTTP_303_SEE_OTHER)
