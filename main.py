import logging

import uvicorn, os
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from portfoliotracker.api import auth_router, stock_router, transaction_router, portfolio_router, company_router, profile_router
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Stock Portfolio Tracker")

logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key="some-random-string"
)

# Mount the static files (css, js, etc.) from the resources/static directory
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "static")), name="static")

templates_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "templates")
templates = Jinja2Templates(directory=templates_directory)


@app.get("/")
async def root(request: Request):
    from portfoliotracker.entities import User
    if request.session["token"]:
        user = User(username = request.session["username"], user_id = request.session['user_id'])
        return templates.TemplateResponse("index.html",{ "request": request, "username": user.username})
    return templates.TemplateResponse("index.html",{ "request": request})


app.include_router(auth_router.router)
app.include_router(transaction_router.router)
app.include_router(portfolio_router.router)
app.include_router(company_router.router)
app.include_router(stock_router.router)
app.include_router(profile_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload  = True)
