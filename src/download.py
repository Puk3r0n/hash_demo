"""
Module responsible for downloading files and calculating their hashes.
"""

import os
import tempfile
import asyncio
import hashlib
import aiofiles
import aiohttp
from loguru import logger


async def download_file(session: aiohttp.ClientSession, file_url: str) -> str:
    """
    Download a file from the given URL using the provided aiohttp session.

    Args:
        session (aiohttp.ClientSession): Aiohttp client session.
        file_url (str): URL of the file to download.

    Returns:
        str: Name of the temporary file where the downloaded content is saved.
    """
    async with session.get(file_url) as response:
        response.raise_for_status()
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        async with aiofiles.open(temp_file.name, 'wb') as file:
            content = await response.read()
            await file.write(content)
        return temp_file.name


async def download_repository_head(session: aiohttp.ClientSession, api_url: str) -> None:
    """
    Download files recursively from the repository API endpoint.

    Args:
        session (aiohttp.ClientSession): Aiohttp client session.
        api_url (str): API URL of the repository.

    """
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
    """
    Calculate SHA256 hashes for a list of files and log the results.

    Args:
        files (list[str]): List of file paths.

    """
    for file in files:
        sha256_hash = hashlib.sha256()
        async with aiofiles.open(file, 'rb') as f:
            while chunk := await f.read(8192):
                sha256_hash.update(chunk)
        logger.info(f'SHA256 hash of {file}: {sha256_hash.hexdigest()}')
        os.remove(file)
