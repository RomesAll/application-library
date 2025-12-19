from fastapi import FastAPI
from schemas import ReaderCreateDTO, ReaderGetDTO, ReaderUpdateDTO, ReaderDeleteDTO
import uvicorn

app = FastAPI()

@app.get('/', description='Вывод всех читателей',
         response_model=ReaderGetDTO, response_model_exclude={'password'})
async def get_all_readers():
    return {'readers': 'get_all_readers'}


@app.get('/{reader_id}', description='Вывод читателя по id',
         response_model=ReaderGetDTO, response_model_exclude={'password'})
async def get_reader_by_id(reader_id: int):
    return {'readers': 'get_reader_by_id'}


@app.post('/', description='Добавить читателя',
          response_model=ReaderCreateDTO, response_model_exclude={'password'})
async def create_reader():
    return {'readers': 'create_reader'}


@app.put('/{reader_id}', description='Обновить читателя',
         response_model=ReaderUpdateDTO, response_model_exclude={'password'})
async def update_reader_by_id(reader_id):
    return {'readers': 'update_reader_by_id'}


@app.delete('/{reader_id}', description='Удалить читателя по id',
            response_model=ReaderDeleteDTO, response_model_exclude={'password'})
async def delete_reader_by_id(reader_id):
    return {'readers': 'delete_reader_by_id'}


if __name__ == '__main__':
    uvicorn.run("api:app", host='0.0.0.0', port=8000, reload=True)
