from .schemas import *
from .repository import ReaderRepositoryAsync
from src.config.models import Readers
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

class ReaderServiceAsync:

    def __init__(self, db_session, request):
        self.db_session: AsyncSession = db_session
        self.request: Request = request

    async def refresh_password(self, id_reader, old_password, new_password):
        result = await ReaderRepositoryAsync(db_session=self.db_session, request=self.request).refresh_password(id_reader, old_password, new_password)
        return result

    #
    async def select_all_records_rel(self, pagination_params: PaginationParams):
        orm_model = await ReaderRepositoryAsync(db_session=self.db_session, request=self.request).select_all_records_rel(pagination_params)
        dto_model = [ReaderRelGetDTO.model_validate(row) for row in orm_model]
        return dto_model

    async def select_all_records(self, pagination_params: PaginationParams):
        orm_model = await ReaderRepositoryAsync(db_session=self.db_session, request=self.request).select_all_records(pagination_params)
        dto_model = [ReaderGetDTO.model_validate(row) for row in orm_model]
        return dto_model

    async def select_record_id_rel(self, reader_id: int):
        orm_model = await ReaderRepositoryAsync(db_session=self.db_session, request=self.request).select_record_id_rel(reader_id)
        dto_model = ReaderRelGetDTO.model_validate(orm_model)
        return dto_model

    async def select_record_id(self, reader_id: int):
        orm_model = await ReaderRepositoryAsync(db_session=self.db_session, request=self.request).select_record_id(reader_id)
        dto_model = ReaderGetDTO.model_validate(orm_model)
        return dto_model

    async def create_record(self, reader: ReaderCreateDTO):
        orm_model = Readers(**reader.model_dump(exclude_none=True))
        result = await ReaderRepositoryAsync(db_session=self.db_session, request=self.request).create_record(orm_model)
        return result

    async def update_record(self, reader: ReaderUpdateDTO):
        orm_model = Readers(**reader.model_dump(exclude_none=True, exclude_defaults=True))
        result = await ReaderRepositoryAsync(db_session=self.db_session, request=self.request).update_record(orm_model)
        return result

    async def delete_record(self, reader_id: int):
        result = await ReaderRepositoryAsync(db_session=self.db_session, request=self.request).delete_record(reader_id)
        return result