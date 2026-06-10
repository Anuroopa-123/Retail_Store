from src.infrastructure.database.seeders.super_admin_seeder import (
    seed_super_admin
)

import asyncio


async def run():

    await seed_super_admin()


if __name__ == "__main__":
    asyncio.run(run())