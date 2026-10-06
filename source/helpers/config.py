from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME:str
    APP_VERSION:str
    ALLOWED_DATATYPE:list
    FILE_MAX_SIZE:int
    FILE_DEFAULT_CHUNK_SIZE:int
    
    MONGODB_URL:str
    MONGODB_DB:str
    model_config=SettingsConfigDict(env_file=".env",env_file_encoding="utf-8")
   
def get_settings():
    return Settings()