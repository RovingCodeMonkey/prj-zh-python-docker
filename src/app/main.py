import logging

from fastapi import FastAPI

from app import utils
from app.routers import common, customers, addresses

logger = logging.getLogger()


app = FastAPI(title="code-challenge", openapi_url="/openapi.json")


@app.exception_handler(Exception)
def generic_exception_handler(request: str, exc: str) -> utils.JSONResponse:
    logger.error(f"unhandled exception: {request}")
    logger.error(str(exc))
    return utils.JSONResponse(content={"message": "server error"}, status_code=500)


app.include_router(common.router)
app.include_router(customers.router)
app.include_router(addresses.router)
