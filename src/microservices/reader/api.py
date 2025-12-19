# import os, sys
# from pathlib import Path
# BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
# sys.path.append(str(BASE_DIR))
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
async def get_all_readers():
    return {'readers': 'get_all_readers'}

@app.get('/{reader_id}')
async def get_reader_by_id(reader_id: int):
    return {'readers': 'get_reader_by_id'}

@app.post('/')
async def create_reader():
    return {'readers': 'create_reader'}

@app.put('/{reader_id}')
async def update_reader_by_id(reader_id):
    return {'readers': 'update_reader_by_id'}

@app.delete('/{reader_id}')
async def delete_reader_by_id(reader_id):
    return {'readers': 'delete_reader_by_id'}

if __name__ == '__main__':
    uvicorn.run("api:app", host='0.0.0.0', port=8000, reload=True)
