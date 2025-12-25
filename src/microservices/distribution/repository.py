from src.config.models.models import Distributions
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.exception_handler import RecordNotFoundError
from src.config import settings
from src.config.schemas.schemas import *
from fastapi import Request

class DistributionRepositoryAsync:

    def __init__(self, db_session, request):
        self.db_session: AsyncSession = db_session
        self.request: Request = request

    async def select_all_distributions(self, pagination_params: PaginationParams):
        query = select(Distributions).limit(pagination_params.limit).offset(pagination_params.offset)
        records = await self.db_session.execute(query)
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - вывел данные о продажах')
        return records.scalars().all()

    async def select_all_distributions_rel(self, pagination_params: PaginationParams):
        query = (
            select(Distributions).limit(pagination_params.limit).offset(pagination_params.offset)
            .options(joinedload(Distributions.book))
            .options(joinedload(Distributions.reader))
            .options(joinedload(Distributions.seller))
        )
        records = await self.db_session.execute(query)
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - вывел данные о продажах')
        return records.scalars().all()

    async def select_distribution_by_id(self, distribution_id: int):
        record = await self.db_session.get(Distributions, {'id': distribution_id})
        if record is None:
            raise RecordNotFoundError(message=f'Продажа с номером: {distribution_id} не найдена')
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - вывел данные о продаже с id: {distribution_id}')
        return record

    async def select_distribution_by_id_rel(self, distribution_id: int):
        query = (
            select(Distributions).filter(Distributions.id == int(distribution_id))
            .options(joinedload(Distributions.book))
            .options(joinedload(Distributions.reader))
            .options(joinedload(Distributions.seller))
        )
        records = await self.db_session.execute(query)
        distribution = records.scalar()
        if distribution is None:
            raise RecordNotFoundError(message=f'Продажа с номером: {distribution_id} не найден')
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - вывел данные о продаже с id: {distribution_id}')
        return distribution

    async def create_distribution(self, orm_model: Distributions):
        self.db_session.add(orm_model)
        await self.db_session.flush()
        await self.db_session.commit()
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - добавил новую запись о продаже')
        return orm_model.id

    async def update_distribution(self, orm_model: Distributions):
        updating_orm_model = await self.db_session.get(Distributions, {'id': orm_model.id})
        if updating_orm_model is None:
            raise RecordNotFoundError(message=f'Продажа с номером: {orm_model.id} не найдена')
        for k,v in orm_model.get_model_attr_without_relations().items():
            if v is not None:
                setattr(updating_orm_model, k, v)
        await self.db_session.commit()
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - обновил данные о продаже с id: {orm_model.id}')
        return orm_model.id

    async def delete_distribution(self, distribution_id: int):
        deleting_orm_model = await self.db_session.get(Distributions, {'id': int(distribution_id)})
        if deleting_orm_model is None:
            raise RecordNotFoundError(message=f'Продажа с номером: {distribution_id} не найдена')
        await self.db_session.delete(deleting_orm_model)
        await self.db_session.commit()
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - удалил данные о продаже с id: {distribution_id}')
        return distribution_id