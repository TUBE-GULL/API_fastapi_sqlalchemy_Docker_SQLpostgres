from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    @property
    def  DATABASE_URL_asyncpg(self)->str:
        #DSN
        #postgresql+psycopg://postgres:postgres@localhost:5432/password
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def  DATABASE_URL_psycopg(self)->str:
        #DSN
        #postgresql+psycopg://postgres:postgres@localhost:5432/password
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    
    model_config = SettingsConfigDict(env_file=".env")
    
settings = Settings()


