# ChatGPT-like UI for AgenticRAG

A modern, responsive chat interface for testing your AgenticRAG application.

## Features
- ✨ Modern ChatGPT-like design
- 🔄 Real-time streaming responses (SSE)
- 💾 Chat history saved locally
- 📱 Responsive mobile design
- 🎨 Beautiful gradient UI with smooth animations

## Quick Start

### 1. Start Your FastAPI Server
```bash
cd AgenticRAGApp
python -m uvicorn main:app --reload
```

The server will start on `http://localhost:8000`

### 2. Open the Chat UI

Choose one of the following:

**Option A: Using the UI endpoint**
```
http://localhost:8000/ui
```

**Option B: Open directly in browser**
- Navigate to `AgenticRAGApp/index.html` and open it in your browser
- The UI will connect to `http://localhost:8000`

## Features

### Chat Functions
- **Send Messages**: Type your question and press Enter or click the send button
- **Streaming**: Responses stream in real-time as they're generated
- **Chat History**: All conversations are saved in your browser's local storage
- **New Chat**: Click the "+ New Chat" button to start a new conversation

### Keyboard Shortcuts
- `Enter`: Send message
- `Shift + Enter`: New line in message
- `Ctrl + C` (in terminal): Stop the server

## Configuration

To change the API endpoint, edit the `API_BASE_URL` in `index.html`:

```javascript
const API_BASE_URL = 'http://localhost:8000'; // Change this if needed
```

To toggle streaming/non-streaming mode:

```javascript
const USE_STREAMING = true; // Set to false to use regular POST
```

## API Endpoints Used

- `POST /chat` - Non-streaming responses
- `POST /chat/stream` - Streaming responses (Server-Sent Events)
- `GET /ui` - Serve this UI

## Troubleshooting

### CORS Errors
The CORS configuration has been updated in `main.py` to allow all origins during development. For production, update:

```python
allow_origins=["your-frontend-domain.com"]
```

### Connection Refused
- Ensure FastAPI server is running: `python -m uvicorn main:app --reload`
- Check that `http://localhost:8000/health` returns `{"status": "healthy"}`

### Messages Not Appearing
- Open browser DevTools (F12) and check the Console tab for errors
- Ensure the chat ID is being generated correctly

## Files

- `index.html` - Complete chat UI with all frontend logic
- `main.py` - FastAPI server with UI endpoint
