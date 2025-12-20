from src.config.models.readers import Readers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class ReaderRepository:

    def __init__(self, db_session):
        self.db_session: AsyncSession = db_session

    async def select_all_reader_async(self):
        query = select(Readers)
        records = await self.db_session.execute(query)
        return records.scalars().all()

    async def select_reader_by_id_async(self, reader_id: int):
        record = await self.db_session.get(Readers, {'id': reader_id})
        return record

    async def create_reader_async(self, orm_model: Readers):
        self.db_session.add(orm_model)
        await self.db_session.flush()
        await self.db_session.commit()
        return orm_model

    async def update_reader_async(self, orm_model: Readers):
        updating_orm_model = await self.db_session.get(Readers, {'id': orm_model.id})
        if updating_orm_model is None:
            pass
        for k,v in orm_model.get_model_attributes().items():
            if v is not None:
                setattr(updating_orm_model, k, v)
        await self.db_session.commit()
        return updating_orm_model

    async def delete_reader_async(self, reader_id: int):
        deleting_orm_model = await self.db_session.get(Readers, {'id': reader_id})
        if deleting_orm_model is None:
            pass
        await self.db_session.delete(deleting_orm_model)
        await self.db_session.commit()
        return deleting_orm_model