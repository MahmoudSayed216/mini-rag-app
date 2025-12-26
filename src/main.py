from fastapi import FastAPI
from helpers.config import get_settings
from routes import base, data


settings = get_settings()

app = FastAPI()
app.include_router(base.base_router)
app.include_router(data.data_router)