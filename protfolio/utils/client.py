from kiteconnect import KiteConnect
from dotenv import load_dotenv
import os
import logging

from modules.auth import app_state

load_dotenv()

kite_api_key = os.getenv("kite_api_key")

def get_kite_client():
    kite = KiteConnect(kite_api_key)
    print(f"{app_state}")
    if "access_token" in app_state:
        kite.set_access_token(app_state["access_token"])
    return kite