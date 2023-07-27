
import logging
import os
from fastapi.responses import RedirectResponse

from fastapi import APIRouter, Request, UploadFile, status
from portfoliotracker.repo.db import get_db_connection
from fastapi.templating import Jinja2Templates
from portfoliotracker.entities import Transaction, User
from portfoliotracker.utils import Settings, get_templates_directory
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
    return templates.TemplateResponse("upload.html", {"request": request})


@router.post("/upload")
def upload(request: Request, file: UploadFile):

    user = User(username = request.session["username"], user_id = request.session['user_id'])

    if not file:
        return templates.TemplateResponse("upload.html", {"request": request, "msg": "No upload file sent!"})

    if file.filename == '':
        return templates.TemplateResponse("upload.html", {"request": request, "msg": "No file selected!"})

    filename = file.filename
    file_location = f"{os.path.join(Settings.CSV_UPLOAD_PATH)}/{user.user_id}_{user.username}_transactions.csv"
   
    if not filename.endswith('.csv'):
        return templates.TemplateResponse("upload.html", {"request": request, "msg": "File should be csv!"})
    try:
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
    except Exception as e:
        return templates.TemplateResponse("upload.html", {"request": request, "msg": str(e)})
    finally:
        file.file.close()

    response = trans_service.upload_transactions(user, file_location)
    if response.error:
        return templates.TemplateResponse("upload.html",{ "request": request, "msg": response.msg})
    return RedirectResponse(url=request.url_for("portfolio"), status_code=status.HTTP_303_SEE_OTHER)
