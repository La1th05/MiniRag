from fastapi import FastAPI
from source.Routes import base
from dotenv import load_dotenv

load_dotenv(".env")

app=FastAPI()

app.include_router(base.router)

