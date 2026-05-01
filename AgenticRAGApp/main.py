from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from response import get_response
from pydantic import BaseModel
import json
from contextlib import asynccontextmanager
from langchain_core.messages import HumanMessage

from graph_client import get_graph

graph = get_graph()

app = FastAPI(title="Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

class AuthRequest(BaseModel):
    mode: str
    email: str
    password: str
    username: str

@app.post("/auth")
async def auth_user(request: AuthRequest):
    """
    Simple authentication endpoint.
    For production, implement proper password hashing and validation.
    """
    email = request.email
    username = request.username
    password = request.password
    mode = request.mode
    
    # Simple validation (replace with real auth logic)
    if not email or not password or len(password) < 6:
        return {"detail": "Invalid email or password"}, 400
    
    # For now, accept any valid email/password combo
    # In production, check against database
    return {
        "token": f"token_{email}_{username}",
        "username": username,
        "email": email,
        "message": f"Successfully {mode}ed as {username}"
    }

class Request(BaseModel):
    question: str
    id: str

@app.post("/chat")
async def chat(request: Request):
    q = request.question
    id = request.id
    response = await get_response(q, id)
    return response

@app.post("/chat/stream")
async def stream_chat(request: Request):
    q = request.question
    q = {"messages": [HumanMessage(content=f"{q}")]}
    id = request.id
    config = {"configurable": {"thread_id": f"{id}"}}
    async def event_generator():
        yield f"data: {json.dumps({'thread_id': id, 'type':'meta'})}\n\n"

        async for event in graph.astream_events(
            input=q, config=config, version="v2"
        ):
            kind = event["event"]
            if kind == "on_chat_model_stream":
                chunk = event["data"]["chunk"].content
                if chunk:
                    yield f"data: {json.dumps({'token': chunk, 'type': 'token'})}\n\n"
        yield f"data: {json.dumps({'type': 'end'})}\n\n"
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"cache-control": "no-cache", "X-Accel-Buffering": "no"}
    )