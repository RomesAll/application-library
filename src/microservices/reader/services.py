from .schemas import *
from .repository import *
from datetime import datetime, timezone
from fastapi import Request

class ReaderService:

    def __init__(self, db_session, request):
        self.db_session: AsyncSession = db_session
        self.request: Request = request

    async def select_all_reader_rel_async(self, pagination_params: PaginationParams):
        orm_model = await ReaderRepository(db_session=self.db_session, request=self.request).select_all_reader_rel_async(pagination_params)
        dto_model = [ReaderRelGetDTO.model_validate(row) for row in orm_model]
        return dto_model

    async def select_all_reader_async(self, pagination_params: PaginationParams):
        orm_model = await ReaderRepository(db_session=self.db_session, request=self.request).select_all_reader_async(pagination_params)
        dto_model = [ReaderGetDTO.model_validate(row) for row in orm_model]
        return dto_model

    async def select_reader_by_id_async(self, reader_id: int):
        orm_model = await ReaderRepository(db_session=self.db_session, request=self.request).select_reader_by_id_async(reader_id)
        dto_model = ReaderGetDTO.model_validate(orm_model)
        return dto_model

    async def create_reader_async(self, reader: ReaderCreateDTO):
        orm_model = Readers(**reader.model_dump(exclude_none=True))
        result = await ReaderRepository(db_session=self.db_session, request=self.request).create_reader_async(orm_model)
        dto_model = ReaderGetDTO.model_validate(result)
        return dto_model

    async def update_reader_async(self, reader: ReaderUpdateDTO):
        orm_model = Readers(**reader.model_dump(exclude_none=True, exclude_defaults=True))
        result = await ReaderRepository(db_session=self.db_session, request=self.request).update_reader_async(orm_model)
        dto_model = ReaderGetDTO.model_validate(result)
        return dto_model

    async def delete_reader_async(self, reader_id: int):
        orm_model = await ReaderRepository(db_session=self.db_session, request=self.request).delete_reader_async(reader_id)
        dto_model = ReaderDeleteDTO.model_validate(orm_model)
        return dto_model