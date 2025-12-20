from fastapi import FastAPI, Depends
from schemas import ReaderCreateDTO, ReaderGetDTO, ReaderUpdateDTO, ReaderDeleteDTO
from services import ReaderService
from depends import db_session
from exception_handler import exception_handler_helper
import uvicorn

app = FastAPI()
exception_handler_helper(app)

@app.get('/', description='Вывод всех читателей')
async def get_all_readers(session: db_session):
    result = await ReaderService(db_session=session).select_all_reader_async()
    return result


@app.get('/{reader_id}', description='Вывод читателя по id')
async def get_reader_by_id(reader_id: int, session: db_session):
    result = await ReaderService(db_session=session).select_reader_by_id_async(reader_id)
    return result


@app.post('/', description='Добавить читателя')
async def create_reader(reader: ReaderCreateDTO, session: db_session):
    result = await ReaderService(db_session=session.get_session_async).create_reader_async(reader)
    return result


@app.put('/{reader_id}', description='Обновить читателя')
async def update_reader_by_id(reader: ReaderUpdateDTO, session: db_session):
    result = await ReaderService(db_session=session.get_session_async).update_reader_async(reader)
    return result


@app.delete('/{reader_id}', description='Удалить читателя по id')
async def delete_reader_by_id(reader_id, session: db_session):
    result = await ReaderService(db_session=session.get_session_async).delete_reader_async(reader_id)
    return result


if __name__ == '__main__':
    uvicorn.run("api:app", host='0.0.0.0', port=8000, reload=True)
