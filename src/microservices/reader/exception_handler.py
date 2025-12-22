from fastapi import Request
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DataError, DBAPIError, IntegrityError, DatabaseError
from src.config import settings

class ReaderNotFoundError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message

def exception_handler_helper(app: FastAPI):

    @app.exception_handler(DatabaseError)
    def database_exception_DatabaseError(request: Request, exc: DatabaseError):
        settings.logging.logger.exception(f'{request.client} - {exc}')
        return JSONResponse(status_code=500, content=str(exc))

    @app.exception_handler(DBAPIError)
    def database_exception_DBAPIError(request: Request, exc: DBAPIError):
        settings.logging.logger.exception(f'{request.client} - {exc}')
        return JSONResponse(status_code=500, content=str(exc))

    @app.exception_handler(IntegrityError)
    def database_exception_IntegrityError(request: Request, exc: IntegrityError):
        settings.logging.logger.exception(f'{request.client} - {exc}')
        return JSONResponse(status_code=400, content=str(exc))

    @app.exception_handler(ValueError)
    def database_exception_ValueError(request: Request, exc: ValueError):
        settings.logging.logger.exception(f'{request.client} - {exc}')
        return JSONResponse(status_code=400, content=str(exc))

    @app.exception_handler(DataError)
    def database_exception_DataError(request: Request, exc: DataError):
        settings.logging.logger.exception(f'{request.client} - {exc}')
        return JSONResponse(status_code=500, content=str(exc))

    @app.exception_handler(Exception)
    def database_exception_Exception(request: Request, exc: Exception):
        settings.logging.logger.exception(f'{request.client} - {exc}')
        return JSONResponse(status_code=500, content=str(exc))

    @app.exception_handler(ReaderNotFoundError)
    def reader_not_found_error(request: Request, exc: ReaderNotFoundError):
        settings.logging.logger.exception(f'{request.client} - {exc}')
        return JSONResponse(status_code=404, content=str(exc))