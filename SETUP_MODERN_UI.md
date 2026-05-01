# AgenticRAG UI - Complete Setup Guide

This workspace now has a **modern React + TypeScript UI** in a separate folder for easy maintenance and upgrades.

## 📁 Project Structure

```
learn/
├── ui/                          # React + Vite frontend
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── services/           # API client
│   │   ├── types/              # TypeScript types
│   │   └── App.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── README.md
├── AgenticRAGApp/               # FastAPI backend
│   ├── main.py
│   ├── graph_client.py
│   ├── response.py
│   └── index.html              # Old HTML UI (you can delete)
└── .venv/                       # Python virtual environment
```

## 🚀 Quick Start

### Option 1: Run Both Dev Servers (Recommended for Development)

#### Terminal 1 - Start Backend

```bash
cd AgenticRAGApp
python -m uvicorn main:app --reload
```

Server runs at `http://localhost:8000`

#### Terminal 2 - Start Frontend

```bash
cd ui
npm install      # First time only
npm run dev
```

UI opens at `http://localhost:5173` with hot reload

### Option 2: Build & Serve UI from Backend

Build the React app and serve it from FastAPI:

```bash
# Build React app
cd ui
npm install
npm run build

# Backend will serve from dist/
cd ../AgenticRAGApp
python -m uvicorn main:app --reload
```

Visit `http://localhost:8000` (backend serves the built UI)

## ✨ What's New

### Frontend (React + TypeScript)

✅ Modern React 18 with hooks  
✅ Full TypeScript support  
✅ Vite for lightning-fast dev experience  
✅ Real-time streaming with SSE  
✅ Chat history with localStorage  
✅ Responsive mobile design  
✅ Beautiful animations  
✅ Easy to upgrade and maintain  

### Why This Stack?

- **React** - Most popular & largest ecosystem
- **TypeScript** - Catch errors before runtime
- **Vite** - 10-100x faster than webpack
- **Modular** - Easy to add features
- **Standards** - Use with any backend

## 📦 Installation Issues?

If you get npm errors:

```bash
cd ui

# Clear cache
npm cache clean --force

# Remove old installations
rm -rf node_modules package-lock.json

# Fresh install
npm install

# Now run
npm run dev
```

## 🔧 Configuration

### API Endpoint

Edit `ui/.env`:

```env
VITE_API_URL=http://localhost:8000
```

### Backend Streaming

The UI expects your `/chat/stream` endpoint to return SSE format:

```javascript
// Each event should be:
data: {"type": "token", "token": "hello"}
data: {"type": "end"}
```

Your `main.py` already supports this! ✓

## 🎯 Next Steps

1. **Install dependencies**: `cd ui && npm install`
2. **Start backend**: `cd AgenticRAGApp && python -m uvicorn main:app --reload`
3. **Start frontend**: `cd ui && npm run dev`
4. **Open**: `http://localhost:5173`

## 📝 Development Workflow

### Adding New Features

1. **Create components** in `src/components/`
2. **Add types** in `src/types/index.ts`
3. **Call API** using `services/api.ts`
4. **Style** with CSS modules

### Example: Adding a Settings Component

```typescript
// src/components/Settings.tsx
export default function Settings() {
  return <div className="settings">...</div>
}

// src/App.tsx
import Settings from './components/Settings'
// Use it...
```

## 🚀 Deployment

### Frontend Only (Recommended)

```bash
cd ui
npm run build
# Deploy dist/ folder to Vercel, Netlify, or any static host
```

### Full Stack

```bash
# Backend: Deploy to Railway, Render, or your server
# Frontend: Deploy dist/ to Vercel, Netlify, or Cloudflare
```

## 📚 Resources

- [React Docs](https://react.dev)
- [Vite Docs](https://vitejs.dev)
- [TypeScript Docs](https://www.typescriptlang.org/docs/)
- [FastAPI + Vite](https://fastapi.tiangolo.com/deployment/concepts/)

## ❓ Troubleshooting

### Port Already in Use

```bash
# Change Vite port in vite.config.ts
server: {
  port: 5174  # Change this
}

# Or kill the process
# Windows: taskkill /PID <pid> /F
# Mac/Linux: kill <pid>
```

### API Connection Error

```bash
# 1. Check backend running
curl http://localhost:8000/health

# 2. Check .env file
cat ui/.env

# 3. Check browser console (F12)
```

### CORS Issues

Already fixed in `AgenticRAGApp/main.py`:

```python
allow_origins=["*"]  # Dev - change for production
```

## 🎓 Learning Resources

The UI is structured to be educational:

- **Components** - Reusable React components
- **Hooks** - useState, useRef, useEffect usage
- **TypeScript** - Interfaces and types
- **CSS** - Modern CSS with animations
- **API Client** - Axios for HTTP requests

Good luck! 🚀
