from urllib.request import Request
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DataError, DBAPIError, IntegrityError, DatabaseError

def exception_handler_helper(app: FastAPI):

    @app.exception_handler(DatabaseError)
    def database_exception_DatabaseError(request: Request, exc: DatabaseError):
        return JSONResponse(status_code=500, content=str(exc))

    @app.exception_handler(DBAPIError)
    def database_exception_DBAPIError(request: Request, exc: DBAPIError):
        return JSONResponse(status_code=500, content=str(exc))

    @app.exception_handler(IntegrityError)
    def database_exception_IntegrityError(request: Request, exc: IntegrityError):
        return JSONResponse(status_code=400, content=str(exc))

    @app.exception_handler(ValueError)
    def database_exception_ValueError(request: Request, exc: ValueError):
        return JSONResponse(status_code=400, content=str(exc))

    @app.exception_handler(DataError)
    def database_exception_DataError(request: Request, exc: DataError):
        return JSONResponse(status_code=500, content=str(exc))

    @app.exception_handler(Exception)
    def database_exception_Exception(request: Request, exc: Exception):
        return JSONResponse(status_code=500, content=str(exc))