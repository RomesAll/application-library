from src.config.models.readers import Readers
from schemas import *
from repository import *
import asyncio

class ReaderService:

    def __init__(self):
        pass

    async def select_all_reader_async(self):
        orm_model = await ReaderRepository().select_all_reader_async()
        dto_model = [ReaderGetDTO.model_validate(row) for row in orm_model]
        return dto_model

    async def select_reader_by_id_async(self, reader_id: int):
        orm_model = await ReaderRepository().select_reader_by_id_async(reader_id)
        dto_model = ReaderGetDTO.model_validate(orm_model)
        return dto_model

    async def create_reader_async(self, reader: ReaderCreateDTO):
        orm_model = Readers(**reader.model_dump(exclude_none=True))
        result = await ReaderRepository().create_reader_async(orm_model)
        dto_model = ReaderGetDTO.model_validate(result)
        return dto_model

    async def update_reader_async(self, reader: ReaderUpdateDTO):
        orm_model = Readers(**reader.model_dump(exclude_none=True, exclude_defaults=True))
        result = await ReaderRepository().update_reader_async(orm_model)
        dto_model = ReaderGetDTO.model_validate(result)
        return dto_model

    async def delete_reader_async(self, reader_id: int):
        orm_model = await ReaderRepository().delete_reader_async(reader_id)
        dto_model = ReaderGetDTO.model_validate(orm_model)
        return dto_model