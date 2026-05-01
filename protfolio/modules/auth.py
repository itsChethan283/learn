from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
import requests
import urllib
from starlette.middleware.sessions import SessionMiddleware
import hashlib
from dotenv import load_dotenv
import logging
import httpx
import os
load_dotenv()

router = APIRouter(tags=["Authentication"])

app_state = {}

kite_api_key = os.getenv("kite_api_key")
kite_api_secret = os.getenv("kite_api_secret")
LOGIN_URL = f"https://kite.zerodha.com/connect/login?api_key={kite_api_key}"

@router.get("/kite_auth")
async def kite_auth():
    login_url = f"https://kite.zerodha.com/connect/login?v=3&api_key={kite_api_key}"
    return RedirectResponse(url=login_url)

@router.get("/callback")
async def kite_callback(request_token: str):
    # Generate checksum: SHA256(api_key + request_token + api_secret)
    checksum_raw = f"{kite_api_key}{request_token}{kite_api_secret}"
    checksum = hashlib.sha256(checksum_raw.encode()).hexdigest()

    # Step 3: POST to get access_token
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.kite.trade/session/token",
            data={
                "api_key": kite_api_key,
                "request_token": request_token,
                "checksum": checksum,
            },
            headers={"X-Kite-Version": "3"},
        )

    data = response.json()
    access_token = data["data"]["access_token"]
    app_state["access_token"] = access_token

    # Save access_token wherever you need (DB, env, memory, etc.)
    return {"access_token": access_token}
    # print(f"{request_token}")
    # # print(f"{request_token}")
    
    # return {"response_token": "generated"}