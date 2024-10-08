from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from nodes.agents.structures import (
    PlannerOutput,
    SelectorOutput,
    ReviewerOutput,
    RouterOutput
)


class AgentGraphState(TypedDict):
    research_question: str
    
    # agents
    planner_response: PlannerOutput
    selector_response: SelectorOutput
    reporter_response: Annotated[list, add_messages]
    reviewer_response: ReviewerOutput
    router_response: RouterOutput
    
    # tools
    serper_response: Annotated[list, add_messages]  # aka search engine results page
    scraper_response: Annotated[list, add_messages]
