from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME:str
    APP_VERSION:str
    ALLOWED_DATATYPE:list
    FILE_MAX_SIZE:int
    FILE_DEFAULT_CHUNK_SIZE:int
    
    MONOGODB_URL:str
    MONGODB_DB:str
    class Config:
        env_file=".env"
   
def get_settings():
    return Settings()