from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_url: str = 'https://gitea.radium.group/api/v1/repos/radium/project-configuration/contents/'


settings = Settings()
