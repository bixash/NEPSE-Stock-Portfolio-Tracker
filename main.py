import logging

import uvicorn, os
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from portfoliotracker.api import auth_router
from portfoliotracker.entities import BaseResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
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
    # return BaseResponse(error=False, msg="OK")
    context = {"name": "World"}
    return templates.TemplateResponse("base.html",{ "request": request, "context": context})


app.include_router(auth_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
