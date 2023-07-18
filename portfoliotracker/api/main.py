import logging

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from portfoliotracker.api import auth_router
from portfoliotracker.entities import BaseResponse

app = FastAPI(title="Stock Portfolio Tracker")

logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def hc():
    return BaseResponse(error=False, msg="OK")


app.include_router(auth_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
