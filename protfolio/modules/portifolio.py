from fastapi import APIRouter
from fastapi.responses import JSONResponse
import requests
import logging
import json
import os
from dotenv import load_dotenv

from .auth import app_state
from utils.client import get_kite_client

router = APIRouter(tags=["Portifolio"])
load_dotenv()

@router.get("/my_portifolio")
def get_portifolio():
    print(f"My Portfolio")
    kite = get_kite_client()
    return JSONResponse(kite.holdings())

@router.get("/orders")
def orders():
    kite = get_kite_client()
    response = requests.get(
        url="https://api.kite.trade/orders",
        headers={
            "X-Kite-Version": "3",
            "Authorization": f'token {os.getenv("kite_api_key")}:{app_state["access_token"]}'
        }
        )
    print(response.content)
    return True