from fastapi import FastAPI
import uvicorn

from modules import portifolio, auth

app = FastAPI(title="Personal Tracker")

app.include_router(portifolio.router)
app.include_router(auth.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8005, reload=True)