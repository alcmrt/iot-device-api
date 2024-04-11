from typing import Optional
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None

    class Config:
        """
        Get configuration variables from .env file
        """
        extra = "allow"
        env_file: str = ".env"



class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False



class DevConfig(GlobalConfig):
    class Config:
        env_prefix: str = "DEV_"



class ProdConfig(GlobalConfig):
    class Config:
        env_prefix: str = "PROD_"



class TestConfig(GlobalConfig):
    DATABASE_URL: str = "sqlite:///test.db"
    #DATABASE_URL: str = "postgresql://posgres:postgres@localhost:5432/test_db"
    DB_FORCE_ROLL_BACK: bool = True

    class Config:
        env_prefix: str = "TEST_"
    


def get_config(env_state: str):
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs[env_state]()


config = get_config(BaseConfig().ENV_STATE)