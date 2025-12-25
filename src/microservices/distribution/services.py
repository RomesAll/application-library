from sqlalchemy.ext.asyncio import AsyncSession

from src.config.schemas.schemas import *
from src.config.models.models import Distributions
from .repository import DistributionRepositoryAsync
from fastapi import Request

class DistributionServiceAsync:

    def __init__(self, db_session, request):
        self.db_session: AsyncSession = db_session
        self.request: Request = request

    async def select_all_distributions(self, pagination_params: PaginationParams):
        orm_model = await DistributionRepositoryAsync(db_session=self.db_session, request=self.request).select_all_distributions(pagination_params)
        dto_model = [DistributionGetDTO.model_validate(row) for row in orm_model]
        return dto_model

    async def select_all_distributions_rel(self, pagination_params: PaginationParams):
        orm_model = await DistributionRepositoryAsync(db_session=self.db_session, request=self.request).select_all_distributions_rel(pagination_params)
        dto_model = [DistributionRelGetDTO.model_validate(row) for row in orm_model]
        return dto_model

    async def select_distribution_by_id(self, distribution_id: int):
        orm_model = await DistributionRepositoryAsync(db_session=self.db_session, request=self.request).select_distribution_by_id(distribution_id)
        dto_model = DistributionGetDTO.model_validate(orm_model)
        return dto_model

    async def select_distribution_by_id_rel(self, distribution_id: int):
        orm_model = await DistributionRepositoryAsync(db_session=self.db_session, request=self.request).select_distribution_by_id_rel(distribution_id)
        dto_model = DistributionRelGetDTO.model_validate(orm_model)
        return dto_model

    async def create_distribution(self, distribution: DistributionCreateDTO):
        orm_model = Distributions(**distribution.model_dump(exclude_none=True))
        result = await DistributionRepositoryAsync(db_session=self.db_session, request=self.request).create_distribution(orm_model)
        return result

    async def update_distribution(self, distribution: DistributionUpdateDTO):
        orm_model = Distributions(**distribution.model_dump(exclude_none=True, exclude_defaults=True))
        result = await DistributionRepositoryAsync(db_session=self.db_session, request=self.request).update_distribution(orm_model)
        return result

    async def delete_distribution(self, distribution_id: int):
        result = await DistributionRepositoryAsync(db_session=self.db_session, request=self.request).delete_distribution(distribution_id)
        return result