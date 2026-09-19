from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    openai_api_key:str
    default_model:str="gpt-5.6-luna"
    judge_model:str="gpt-5.6-luna"
    database_url:str="postgresql+asyncpg://eval:eval@localhost:5432/eval"
    redis_url:str="redis://localhost:6379/0"
    java_evaluator_url:str="http://localhost:8081"
    otel_exporter_otlp_endpoint:str="http://localhost:4318"
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
settings=Settings()
