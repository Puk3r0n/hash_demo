import os
import tempfile
import asyncio
import hashlib
import aiofiles
import aiohttp
from loguru import logger
from .settings import settings


async def download_file(session: aiohttp.ClientSession, file_url: str) -> str:
    async with session.get(file_url) as response:
        response.raise_for_status()
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        async with aiofiles.open(temp_file.name, 'wb') as file:
            content = await response.read()
            await file.write(content)
        return temp_file.name


async def download_repository_head(session: aiohttp.ClientSession, api_url: str) -> None:
    async with session.get(api_url) as response:
        response.raise_for_status()
        files = await response.json()

        if not isinstance(files, list):
            logger.error(f"Unexpected response format: {files}")
            return

        tasks = []
        for file in files:
            if file['type'] == 'file':
                tasks.append(download_file(session, file['download_url']))
                if len(tasks) == 3:
                    results = await asyncio.gather(*tasks)
                    await calculate_hashes(results)
                    tasks.clear()
            elif file['type'] == 'dir':
                await download_repository_head(session, file['url'])

        if tasks:
            results = await asyncio.gather(*tasks)
            await calculate_hashes(results)


async def calculate_hashes(files: list[str]) -> None:
    for file in files:
        sha256_hash = hashlib.sha256()
        async with aiofiles.open(file, 'rb') as f:
            while chunk := await f.read(8192):
                sha256_hash.update(chunk)
        logger.info(f'SHA256 hash of {file}: {sha256_hash.hexdigest()}')
        os.remove(file)
