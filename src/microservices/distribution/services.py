from .schemas import *
from .repository import *
from fastapi import Request

class DistributionService:

    def __init__(self, db_session, request):
        self.db_session: AsyncSession = db_session
        self.request: Request = request

    async def select_all_distribution_async(self, pagination_params: PaginationParams):
        orm_model = await DistributionRepository(db_session=self.db_session, request=self.request).select_all_distribution_async(pagination_params)
        dto_model = [DistributionGetDTO.model_validate(row) for row in orm_model]
        return dto_model

    async def select_distribution_by_id_async(self, distribution_id: int):
        orm_model = await DistributionRepository(db_session=self.db_session, request=self.request).select_distribution_by_id_async(distribution_id)
        dto_model = DistributionGetDTO.model_validate(orm_model)
        return dto_model

    async def create_distribution_async(self, distribution: DistributionCreateDTO):
        orm_model = Distributions(**distribution.model_dump(exclude_none=True))
        result = await DistributionRepository(db_session=self.db_session, request=self.request).create_distribution_async(orm_model)
        dto_model = DistributionGetDTO.model_validate(result)
        return dto_model

    async def update_distribution_async(self, distribution: DistributionUpdateDTO):
        orm_model = Distributions(**distribution.model_dump(exclude_none=True, exclude_defaults=True))
        result = await DistributionRepository(db_session=self.db_session, request=self.request).update_distribution_async(orm_model)
        dto_model = DistributionGetDTO.model_validate(result)
        return dto_model

    async def delete_distribution_async(self, distribution_id: int):
        orm_model = await DistributionRepository(db_session=self.db_session, request=self.request).delete_distribution_async(distribution_id)
        dto_model = DistributionDeleteDTO.model_validate(orm_model)
        return dto_model