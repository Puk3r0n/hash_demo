import asyncio
import aiohttp
from src.download import download_repository_head
from src.settings import settings


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        await download_repository_head(session, settings.api_url)


if __name__ == '__main__':
    asyncio.run(main())