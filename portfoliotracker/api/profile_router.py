import logging

from fastapi import APIRouter, Request, Form, status, Response
from fastapi.responses import RedirectResponse


from portfoliotracker.entities import BaseResponse, User
from portfoliotracker.entities.auth import LoginRequest, SignupRequest
from portfoliotracker.repo.user_repo import UserRepo
from portfoliotracker.repo.db import get_db_connection
from portfoliotracker.service.user_service import UserService
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

router = APIRouter()

logger = logging.getLogger(__name__)

db = get_db_connection()
user_repo = UserRepo(db)
user_service = UserService(user_repo=user_repo)



templates_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "resources", "templates")
templates = Jinja2Templates(directory=templates_directory)

@router.get('/profile')
def profile(request: Request):


    if not request.session["token"]:
        return  templates.TemplateResponse("login.html", { "request": request, "msg":"Please login to continue!"})
   
    user = User(username = request.session["username"], user_id = request.session['user_id'])

    response = user_service.get_user(user.user_id).result
  
    return templates.TemplateResponse("profile.html", { "request": request,  "user_id": user.user_id, "username": user.username,"password":response.password, "email": response.email})



@router.post('/profile/change-username')
def change_username(request: Request, username: str = Form(), password: str = Form()):
    if not request.session["token"]:
        return  templates.TemplateResponse("login.html", { "request": request, "msg":"Please login to continue!"})
    
    user = User(username = request.session["username"], user_id = request.session['user_id'])

    response = user_service.get_user(user.user_id).result
    real_pass = response.password
    typed_pass = password
  

    if real_pass == typed_pass:
        response = user_service.update_user_username(username, user.user_id)
        if response.error:
            return templates.TemplateResponse("profile.html",{ "request": request, "msg": response.msg})
        
        request.session["username"] = username
        return RedirectResponse(url=request.url_for("profile"), status_code=status.HTTP_303_SEE_OTHER, headers={"msg":"Username updated!"})
    
        # return templates.TemplateResponse("profile.html",{ "request": request, "msg": "Username updated!"})
    else:
        return templates.TemplateResponse("profile.html", { "request": request,  "user_id": user.user_id, "username": user.username,"password":response.password, "email": response.email, "msg": "Sorry password invalid!"})

@router.post('/profile/change-email')
def change_email(request: Request, email: str = Form(), password: str = Form()):
    if not request.session["token"]:
        return  templates.TemplateResponse("login.html", { "request": request, "msg":"Please login to continue!"})
    
    user = User(username = request.session["username"], user_id = request.session['user_id'])

    response = user_service.get_user(user.user_id).result
    real_pass = response.password
    typed_pass = password
  

    if real_pass == typed_pass:
        response = user_service.update_user_email(email, user.user_id)
        if response.error:
            return templates.TemplateResponse("profile.html",{ "request": request, "msg": response.msg})
        
        return RedirectResponse(url=request.url_for("profile"), status_code=status.HTTP_303_SEE_OTHER, headers={"msg":"Email updated!"})
    
        # return templates.TemplateResponse("profile.html",{ "request": request, "msg": "email updated!"})
    else:
        return templates.TemplateResponse("profile.html", { "request": request,  "user_id": user.user_id, "username": user.username,"password":response.password, "email": response.email, "msg": "Sorry password invalid!"})

@router.post('/profile/change-password')
def change_password(request: Request, new_password: str = Form(), password: str = Form()):
    if not request.session["token"]:
        return  templates.TemplateResponse("login.html", { "request": request, "msg":"Please login to continue!"})
    
    user = User(username = request.session["username"], user_id = request.session['user_id'])

    response = user_service.get_user(user.user_id).result
    real_pass = response.password
    typed_pass = password

    if real_pass == typed_pass:
        response = user_service.update_user_password(new_password, user.user_id)
        if response.error:
            return templates.TemplateResponse("login.html",{ "request": request, "msg": response.msg})
        
        return RedirectResponse(url=request.url_for("profile"), status_code=status.HTTP_303_SEE_OTHER, headers={"msg":"Password updated!"})
        
    else:
        return templates.TemplateResponse("profile.html", { "request": request,  "user_id": user.user_id, "username": user.username,"password":response.password, "email": response.email, "msg": "Sorry password invalid!"})
 
        

    




