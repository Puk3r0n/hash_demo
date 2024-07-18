from src.settings import settings


def test_settings():
    assert settings.api_url == 'https://gitea.radium.group/api/v1/repos/radium/project-configuration/contents/'
