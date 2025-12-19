from src.config import session_factory_async
from src.config.models.readers import Readers
from sqlalchemy import select

class ReaderRepository:

    def __init__(self):
        pass

    async def select_all_reader_async(self):
        async with session_factory_async() as session:
            query = select(Readers)
            records = await session.execute(query)
            return records.scalars().all()

    async def select_reader_by_id_async(self, reader_id: int):
        async with session_factory_async() as session:
            record = await session.get(Readers, {'id': reader_id})
            return record

    async def create_reader_async(self, orm_model: Readers):
        async with session_factory_async() as session:
            session.add(orm_model)
            await session.flush()
            await session.commit()
            return orm_model

    async def update_reader_async(self, orm_model: Readers):
        async with session_factory_async() as session:
            updating_orm_model = await session.get(Readers, {'id': orm_model.id})
            if updating_orm_model is None:
                pass
            for k,v in orm_model.get_model_attributes().items():
                if v is not None:
                    setattr(updating_orm_model, k, v)
            await session.commit()
            return updating_orm_model

    async def delete_reader_async(self, reader_id: int):
        async with session_factory_async() as session:
            deleting_orm_model = await session.get(Readers, {'id': reader_id})
            if deleting_orm_model is None:
                pass
            await session.delete(deleting_orm_model)
            await session.commit()
            return deleting_orm_model