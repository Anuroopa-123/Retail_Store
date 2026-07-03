from src.persistence.admin_profile_repository import (
    AdminProfileRepository
)


class AdminProfileService:

    def __init__(self, db):

        self.repo = AdminProfileRepository(db)

    async def get_profile(
        self,
        user_id
    ):

        return await self.repo.get_profile(
            user_id
        )

    async def update_profile(
        self,
        user,
        data
    ):

        return await self.repo.create_or_update(
            user,
            data
        )
    async def update_photo(

    self,

    user,

    photo

    ):

        return await self.repo.update_photo(

            user,

            photo

        )

   