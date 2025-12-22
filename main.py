from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
# from src.microservices.reader import router as reader_router
# from src.microservices.users import router as users_router
from src.microservices.distribution import router as distribution_router
from src.config import exception_handler_helper
from src.config import settings
import uvicorn

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True)

exception_handler_helper(app)

# app.include_router(reader_router)
# app.include_router(users_router)
app.include_router(distribution_router)

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    settings.logging.logger.info(f'{request.client.host} - {request.method} - запрос пришел на обработку в сервис')
    response = await call_next(request)
    settings.logging.logger.info(f'{request.client.host} - {request.method} - запрос был успешно обработан в сервисе')
    return response

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)