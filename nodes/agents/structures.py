from pydantic import BaseModel, Field
from typing import Annotated, List, Literal
from langgraph.graph.message import add_messages


class PlannerOutput(BaseModel):
    search_term: str = Field(
        description="The most relevant search term to start with",
    )
    overall_strategy: str = Field(
        description="The overall strategy to guide the search process"
    )
    additional_information: Annotated[List[str], add_messages] = Field(
        description="Any additional information to guide the search including other search terms or filters"
    )


class SelectorOutput(BaseModel):
    selected_page_url: str = Field(
        description="The exact URL of the page you selected"
    )
    description: str = Field(
        description="A brief description of the page"
    )
    reason_for_selection: str = Field(
        description="Why you selected this page"
    )


class ReviewerOutput(BaseModel):
    feedback: str = Field(
        description="precise feedback on what is required to pass the review."
    )
    pass_review: Literal["True", "False"] = Field(
        description="whether the review will pass or not."
    )
    comprehensive: Literal["True", "False"] = Field(
        description="whether the review is comprehensive."
    )
    citations_provided: Literal["True", "False"] = Field(
        description="whether citations are provided."
    )
    relevant_to_research_question: Literal["True", "False"] = Field(
        description="whether the report is relevant to the research question."
    )


class RouterOutput(BaseModel):
    next_agent: Literal["planner", "selector", "reporter", "print_report"] = Field(
        description="the next node of the graph to be executed."
    )
