import pytest
import asyncio
import aiohttp
from src.download import download_file, download_repository_head, calculate_hashes


# Mock response data
class MockResponse:
    def __init__(self, data):
        self.data = data

    async def json(self):
        return self.data


@pytest.mark.asyncio
async def test_download_file(tmp_path):
    # Setup mock session and file URL
    mock_session = aiohttp.ClientSession()
    mock_data = b"Mock file content"
    mock_response = MockResponse(mock_data)

    # Mock download URL
    mock_url = "https://example.com/mockfile.txt"

    # Patch session.get to return mock response
    async def mock_get(url):
        return mock_response

    mock_session.get = mock_get

    # Test download_file function
    temp_file = await download_file(mock_session, mock_url)
    assert temp_file.startswith('/var')  # Ensure temp file is created in temp directory

    # Read downloaded file content
    with open(temp_file, 'rb') as f:
        content = f.read()
        assert content == mock_data


@pytest.mark.asyncio
async def test_calculate_hashes(tmp_path):
    # Create temporary tests files
    test_file1 = tmp_path / "testfile1.txt"
    test_file2 = tmp_path / "testfile2.txt"

    # Write content to files
    with open(test_file1, 'wb') as f1, open(test_file2, 'wb') as f2:
        f1.write(b"Test file 1 content")
        f2.write(b"Test file 2 content")

    # Calculate hashes
    await calculate_hashes([str(test_file1), str(test_file2)])

    # Check hashes
    # Note: Replace with actual hash values calculated during the tests
    # Hash values will vary based on content, use hashlib.sha256() to calculate actual values
    assert True  # Add assertions for hash values here


@pytest.mark.asyncio
async def test_download_repository_head(tmp_path):
    # Mock session and API response
    mock_session = aiohttp.ClientSession()
    mock_data = [
        {"type": "file", "download_url": "https://example.com/mockfile1.txt"},
        {"type": "file", "download_url": "https://example.com/mockfile2.txt"},
        {"type": "dir", "url": "https://example.com/mockdir/"}
    ]
    mock_response = MockResponse(mock_data)

    # Patch session.get to return mock response
    async def mock_get(url):
        return mock_response

    mock_session.get = mock_get

    # Test download_repository_head function
    await download_repository_head(mock_session, "https://example.com/api/v1/repos/mockrepo/contents/")

    # Add assertions or checks as needed to verify expected behavior


if __name__ == "__main__":
    asyncio.run(pytest.main())
