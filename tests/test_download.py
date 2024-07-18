from loguru import logger
import pytest
import aiohttp
import os
import tempfile
from src.download import download_file, download_repository_head, calculate_hashes


@pytest.mark.asyncio
async def test_download_file():
    async with aiohttp.ClientSession() as session:
        file_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"  # Replace with a valid URL for testing
        temp_file = await download_file(session, file_url)
        assert temp_file is not None
        assert os.path.exists(temp_file)
        os.remove(temp_file)


@pytest.mark.asyncio
async def test_calculate_hashes():
    log_file_path = "test.log"

    # Setting up logging
    logger.add(log_file_path)

    # Create a temporary file and get its name
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file_name = temp_file.name

    try:
        # Writing test content to the temporary file
        temp_file.write(b"test content")
        temp_file.flush()  # Ensure all data is written before closing
        temp_file.close()  # Close the file explicitly

        # Call the function that should log
        await calculate_hashes([temp_file_name])

        # Check for the presence of the log file
        assert os.path.isfile(log_file_path)

        # Check the content of the log file
        log_contents = open(log_file_path).read()
        assert "SHA256 hash of" in log_contents

    finally:
        # Remove the temporary file
        os.remove(temp_file.name)

        # Remove the log file
        os.remove(log_file_path)




@pytest.mark.asyncio
async def test_download_repository_head():
    async with aiohttp.ClientSession() as session:
        api_url = "https://gitea.radium.group/api/v1/repos/radium/project-configuration/contents/"
        await download_repository_head(session, api_url)
        # Add assertions based on expected behavior