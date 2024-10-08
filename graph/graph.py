from langgraph.graph import StateGraph, START, END
from states.states import AgentGraphState
from nodes.agents.agents import (
    planner,
    selector,
    reporter,
    reviewer,
    router,
)
from nodes.tools.tools import (
    google_serper,
    scrape_website,
    print_report,
    routing,
)


def create_graph():
    graph = StateGraph(AgentGraphState)

    graph.add_node("planner", planner)
    graph.add_node("websearch", google_serper)
    graph.add_node("selector", selector)
    graph.add_node("scrape_website", scrape_website)
    graph.add_node("reporter", reporter)
    graph.add_node("reviewer", reviewer)
    graph.add_node("router", router)
    graph.add_node("print_report", print_report)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "websearch")
    graph.add_edge("websearch", "selector")
    graph.add_edge("selector", "scrape_website")
    graph.add_edge("scrape_website", "reporter")
    graph.add_edge("reporter", "reviewer")
    graph.add_edge("reviewer", "router")
    graph.add_conditional_edges(
        "router", routing,
        {
            "planner": "planner",
            "selector": "selector",
            "reporter": "reporter",
            "print_report": "print_report"
        }
    )
    graph.add_edge("print_report", END)
    
    return graph.compile()