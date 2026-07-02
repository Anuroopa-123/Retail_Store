from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.admin.admin_profile import AdminProfile

from src.domain.entities.user import User


class AdminProfileRepository:

    def __init__(self, db: AsyncSession):

        self.db = db

    async def get_profile(self, user_id: int):

        result = await self.db.execute(

            select(AdminProfile)

            .where(
                AdminProfile.user_id == user_id
            )
        )

        return result.scalar_one_or_none()
    
    

    async def create_or_update(
        self,
        user: User,
        data
    ):

        profile = await self.get_profile(
            user.id
        )

        if not profile:

            profile = AdminProfile(

                user_id=user.id
            )

            self.db.add(profile)

        profile.phone = data.phone

        profile.gender = data.gender

        profile.dob = data.dob

        profile.address = data.address

        profile.city = data.city

        profile.state = data.state

        profile.country = data.country

        profile.pincode = data.pincode

        profile.photo = data.photo

        await self.db.commit()

        await self.db.refresh(profile)

        return profile
    
    async def update_photo(

    self,

    user,

    photo

    ):

        profile = await self.get_profile(
        user.id
        )

        if not profile:

            profile = AdminProfile(

                user_id=user.id

            )

            self.db.add(profile)

        profile.photo = photo

        await self.db.commit()

        await self.db.refresh(profile)

        return profile