from schemas import *
from repository import *

class ReaderService:

    def __init__(self, db_session):
        self.db_session: AsyncSession = db_session

    async def select_all_reader_async(self):
        orm_model = await ReaderRepository(db_session=self.db_session).select_all_reader_async()
        dto_model = [ReaderGetDTO.model_validate(row) for row in orm_model]
        return dto_model

    async def select_reader_by_id_async(self, reader_id: int):
        orm_model = await ReaderRepository(db_session=self.db_session).select_reader_by_id_async(reader_id)
        dto_model = ReaderGetDTO.model_validate(orm_model)
        return dto_model

    async def create_reader_async(self, reader: ReaderCreateDTO):
        orm_model = Readers(**reader.model_dump(exclude_none=True))
        result = await ReaderRepository(db_session=self.db_session).create_reader_async(orm_model)
        dto_model = ReaderGetDTO.model_validate(result)
        return dto_model

    async def update_reader_async(self, reader: ReaderUpdateDTO):
        orm_model = Readers(**reader.model_dump(exclude_none=True, exclude_defaults=True))
        result = await ReaderRepository(db_session=self.db_session).update_reader_async(orm_model)
        dto_model = ReaderGetDTO.model_validate(result)
        return dto_model

    async def delete_reader_async(self, reader_id: int):
        orm_model = await ReaderRepository(db_session=self.db_session).delete_reader_async(reader_id)
        dto_model = ReaderGetDTO.model_validate(orm_model)
        return dto_model