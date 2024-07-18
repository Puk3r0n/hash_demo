"""
Module responsible for defining project settings.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings class defining configuration parameters for the project.

    Attributes:
        api_url (str): Default API URL for project-related content.
    """
    api_url: str = 'https://gitea.radium.group/api/v1/repos/radium/project-configuration/contents/'


settings = Settings()
