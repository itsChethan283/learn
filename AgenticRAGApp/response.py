from graph_client import get_graph
from langchain_core.messages import HumanMessage
from typing import TypedDict

graph = get_graph()
#response.py

class Portifolio(TypedDict):
    symbol: str
    exchange: str
    quantity: int
    average_price: float



async def get_response(q, id):
    config = {"configurable": {"thread_id": f"{id}"}}
    q = {"input": [HumanMessage(content=f"{q}")]}
    graph_r = await graph.ainvoke(q, config=config)
    r = graph_r["messages"][-1]
    # print(len(graph_r["messages"]))
    # print(r.content)
    return r.content