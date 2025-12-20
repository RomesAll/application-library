from fastapi import FastAPI, Depends
from schemas import ReaderCreateDTO, ReaderGetDTO, ReaderUpdateDTO, ReaderDeleteDTO
from services import ReaderService
from src.config import db_helper
import uvicorn, os, sys
print(sys.path)

app = FastAPI()

@app.get('/', description='Вывод всех читателей')
async def get_all_readers(db_session = Depends(db_helper.get_session_async)):
    result = await ReaderService(db_session=db_session).select_all_reader_async()
    return result


@app.get('/{reader_id}', description='Вывод читателя по id')
async def get_reader_by_id(reader_id: int, db_session = Depends(db_helper.get_session_async)):
    result = await ReaderService(db_session=db_session).select_reader_by_id_async(reader_id)
    return result


@app.post('/', description='Добавить читателя')
async def create_reader(reader: ReaderCreateDTO, db_session = Depends(db_helper.get_session_async)):
    result = await ReaderService(db_session=db_session).create_reader_async(reader)
    return result


@app.put('/{reader_id}', description='Обновить читателя')
async def update_reader_by_id(reader: ReaderUpdateDTO, db_session = Depends(db_helper.get_session_async)):
    result = await ReaderService(db_session=db_session).update_reader_async(reader)
    return result


@app.delete('/{reader_id}', description='Удалить читателя по id')
async def delete_reader_by_id(reader_id, db_session = Depends(db_helper.get_session_async)):
    result = await ReaderService(db_session=db_session).delete_reader_async(reader_id)
    return result


if __name__ == '__main__':
    uvicorn.run("api:app", host='0.0.0.0', port=8000, reload=True)
