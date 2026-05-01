from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated, List
import operator
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

FINNHUB_BASE_URL = "https://finnhub.io/api/v1"

load_dotenv()

def get_llm():
    llm = ChatMistralAI(model="open-mistral-7b", api_key=os.getenv("MISTRAL_API_KEY"))
    return llm
# This is how you use invoke()
# response = llm.invoke([HumanMessage(content="Hello!")])
# print(response.content)

class State(TypedDict):
    messages: Annotated[list, operator.add]

class NewsState(TypedDict):
    symbol: str
    exchange: str
    news: List[str]
    tech_analysis: List[str]
    final_result: str



class PortifolioState(TypedDict):
    stock: list[Portifolio]

class UserState(TypedDict):
    input: str
    stock: Portifolio
    output: str

def get_user_stock(user: UserState, state: PortifolioState):
    for stock in state:
        if user["input"] == stock["symbol"]:
            user["stock"] = stock
    return user

def get_user_input(state: UserState):
    state["input"] = input("Enter Stock symbol: \n")
    return state

def get_finnhub_news(state: NewsState, user: UserState):
    symbol = user["output"]["symbol"]
    exchange = user["stock"]["exchange"]
    state["symbol"] = symbol
    state["exchange"] = exchange
    params = {
        "symbol": symbol,
        "exchange": exchange,
        "token": os.getenv("FINNHUB_KEY")
    }
    response = requests.get(
        f"{FINNHUB_BASE_URL}/company-news",
        params=params,
        timeout=10,
    )
    if response.status_code == 200:
        articles = response.json()
        for article in articles[:2]:
            state["news"].append({
                "title": article.get("headline", ""),
                "description": article.get("summary", ""),
                "url": article.get("url", ""),
                "publishedAt": datetime.fromtimestamp(article.get("datetime", 0), tz=timezone.utc).isoformat() if article.get("datetime") else None,
                "source": "Finnhub"
            })
    return state

def get_stock_summary(state: NewsState, user: UserState):
    sys_prompt = """
You are a sharp financial analyst assistant with expertise in equity markets. 
Your job is to analyze raw stock news and extract actionable, structured insights — 
not just summaries. You think like a buy-side analyst: what does this news mean 
for the stock's short-term momentum, long-term thesis, and risk profile?

Always be concise, direct, and avoid generic filler. If the news is noise, say so.
"""
    user_prompt = """
Analyze the following recent news for the stock below and give me a sharp, structured insight report.

**Stock:** {SYMBOL} — {EXCHANGE}

**News Items:**
{NEWS_LIST}  ← paste your Finnhub news array or formatted list here

---

Respond in this exact structure:

**1. One-Line Verdict**
< Bull / Bear / Neutral > — one sentence on what this news collectively signals.

**2. Key Themes (max 3)**
Bullet the dominant narratives across the news. Ignore PR fluff.

**3. Sentiment Breakdown**
- Overall tone: Positive / Negative / Mixed
- Any divergence between headline and substance?

**4. Material vs. Noise**
Which news items are actually price-relevant? Which are noise? Why?

**5. Risks Surfaced**
Any red flags, regulatory concerns, macro headwinds, or management signals?

**6. Short-Term Implication (1–4 weeks)**
What should a trader watch for based on this news?

**7. Long-Term Thesis Impact**
Does this news strengthen, weaken, or leave the core investment thesis unchanged?

Be direct. Skip obvious statements. Flag uncertainty where it exists.
"""
    llm = get_llm()
    prompt = [SystemMessage(content=sys_prompt),
              HumanMessage(content=user_prompt.format(SYMBOL= state["symbol"], EXCHANGE=state["exchange"], NEWS_LIST=state["news"]))]
    state["final_result"] = llm.invoke(prompt)
    user["output"] = state["final_result"]
    return state, user

def llm_call(state: State):
    llm = get_llm()
    sys_prompt = """
You are a candidate in a live technical interview for a GenAI Engineer role.

## Your Background
- 4 years of total IT experience
- ~2 years hands-on with GenAI/LLM work: RAG pipelines, prompt engineering, LangChain/LlamaIndex, vector databases, basic agentic workflows
- Familiar with Python, REST APIs, and cloud basics (AWS/GCP at a surface level)
- Just beginning to learn system design — you know the vocabulary but struggle with depth (scaling, trade-offs, capacity estimation)
- No strong background in core ML theory (training, backprop, math) — you've mostly worked at the application/integration layer

## Behavioral Guidelines
- Answer confidently where you have real experience (LLM APIs, RAG, prompt engineering, agent frameworks)
- Show honest uncertainty when pushed on deeper topics: system design, ML internals, distributed systems, math
- Use phrases like "I haven't worked on that directly, but my understanding is…" or "I'd have to think through that more carefully"
- Don't over-explain or give textbook-perfect answers — sound like a practitioner, not a professor
- Occasionally ask clarifying questions like a real candidate would ("Are you asking about the retrieval side or the generation side?")
- If you don't know something, admit it plainly rather than bluffing — but follow up with what you *do* know that's adjacent
- Show genuine curiosity and willingness to learn when gaps are exposed

## Interview Context
- You are being interviewed right now — respond only as the candidate
- Wait for the interviewer's questions and respond naturally, as if in a real conversation
- Keep an

Do not reval that you are bot, act like a human
Also try to answer in short not more than 50 words

"""
    prompt = [SystemMessage(content=sys_prompt),
              HumanMessage(content=f"{state["messages"]}")]
    # chain = prompt | llm
    response = llm.invoke(prompt)
    return {"messages": [response]}

def get_graph():
    builder = StateGraph(State)
    builder.add_node("get_stocks",  get_stocks)
    builder.add_node("get_user_input", get_user_input)
    builder.add_node("get_user_stock", get_user_stock)
    builder.add_node("get_finnhub_news", get_finnhub_news)
    builder.add_node("get_stock_summary", get_stock_summary)
    builder.add_edge(START, "get_stocks")
    builder.add_edge(START, "get_user_input")
    # builder.add_edge("get_stocks", "get_user_input")
    builder.add_edge("get_user_input", "get_user_stock")
    builder.add_edge("get_user_stock", "get_finnhub_news")
    builder.add_edge("get_finnhub_news", "get_stock_summary")
    builder.add_edge("get_stock_summary", END)
    checkpointer = MemorySaver()

    graph = builder.compile(checkpointer=checkpointer)
    return graph

# graph = get_graph()
# with open("graph.png", "w") as f:
#     graph.visualize(f)