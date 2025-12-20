from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.microservices.reader import router as reader_router
from src.microservices.reader import exception_handler_helper
import uvicorn

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True)

exception_handler_helper(app)

app.include_router(reader_router)


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)