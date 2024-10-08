from states.states import AgentGraphState
from langchain_core.messages import SystemMessage, HumanMessage
from nodes.agents.structures import (
    PlannerOutput,
    SelectorOutput,
    ReviewerOutput,
    RouterOutput
)
from prompts.prompts import (
    planner_prompt_template,
    selector_prompt_template,
    reporter_prompt_template,
    reviewer_prompt_template,
    router_prompt_template,
)
from utils.utils import get_current_utc_datetime
from langchain_openai import ChatOpenAI


MODEL = "gpt-4o-mini"
TEMPERATURE = 0


def planner(state: AgentGraphState):
    reviewer_response =  state.get("reviewer_response", None)
    if not reviewer_response:
        feedback = None
    else:
        feedback = reviewer_response.feedback

    planner_prompt = planner_prompt_template.format(
        feedback=feedback,
        datetime=get_current_utc_datetime()
    )

    messages = [
        SystemMessage(content=planner_prompt),
        HumanMessage(content=f"research_question: {state['research_question']}")
    ]

    llm = ChatOpenAI(model=MODEL, temperature=TEMPERATURE)
    structured_planner_llm = llm.with_structured_output(PlannerOutput)
    return {"planner_response": structured_planner_llm.invoke(messages)}


def selector(state: AgentGraphState):
    reviewer_response =  state.get("reviewer_response", None)
    if not reviewer_response:
        feedback = None
    else:
        feedback = reviewer_response.feedback
    
    previous_selections = state.get("selector_response", None)
    if not previous_selections:
        previous_selections = None
    else:
        previous_selections = previous_selections.selected_page_url
    
    selector_prompt = selector_prompt_template.format(
        serp=state["serper_response"],  # search engine results
        feedback=feedback,
        previous_selections=previous_selections,
        datetime=get_current_utc_datetime()
    )

    messages = [
        SystemMessage(content=selector_prompt),
        HumanMessage(content=f"research_question: {state['research_question']}")
    ]

    llm = ChatOpenAI(model=MODEL, temperature=TEMPERATURE)
    structured_selector_llm = llm.with_structured_output(SelectorOutput)
    return {"selector_response": structured_selector_llm.invoke(messages)}


def reporter(state: AgentGraphState):
    
    reviewer_response =  state.get("reviewer_response", None)
    if not reviewer_response:
        feedback = None
    else:
        feedback = reviewer_response.feedback

    previous_selections = state.get("selector_response", None)
    if not previous_selections:
        previous_selections = None
    else:
        previous_selections = previous_selections.selected_page_url
    
    research = "\n\n".join(scrape.content for scrape in state["scraper_response"])
    
    reporter_prompt = reporter_prompt_template.format(
        research=research,
        feedback=feedback,
        previous_reports=previous_selections,
        datetime=get_current_utc_datetime(),
    )

    messages = [
        SystemMessage(content=reporter_prompt),
        HumanMessage(content=f"research_question: {state['research_question']}")
    ]

    researcher_llm = ChatOpenAI(model=MODEL, temperature=TEMPERATURE)
    return {"reporter_response": researcher_llm.invoke(messages)}


def reviewer(state: AgentGraphState):
    
    reviewer_response =  state.get("reviewer_response", None)
    if not reviewer_response:
        feedback = None
    else:
        feedback = reviewer_response.feedback

    reporter = "\n\n".join(report.content for report in state["reporter_response"])

    reviewer_prompt = reviewer_prompt_template.format(
        reporter=reporter,
        feedback=feedback,
        datetime=get_current_utc_datetime()
    )

    messages = [
        SystemMessage(content=reviewer_prompt),
        HumanMessage(content=f"research_question: {state['research_question']}")
    ]

    llm = ChatOpenAI(model=MODEL, temperature=TEMPERATURE)
    structured_reviewer_llm = llm.with_structured_output(ReviewerOutput)
    return {"reviewer_response": structured_reviewer_llm.invoke(messages)}


def router(state: AgentGraphState):
    reviewer_response =  state.get("reviewer_response", None)
    if not reviewer_response:
        feedback = None
        pass_review = None
    else:
        feedback = reviewer_response.feedback
        pass_review = reviewer_response.pass_review

    router_prompt = router_prompt_template.format(
        feedback=feedback,
        pass_review=pass_review
    )

    messages = [
        SystemMessage(content=router_prompt),
        HumanMessage(content=f"research_question: {state['research_question']}")
    ]
    
    llm = ChatOpenAI(model=MODEL, temperature=TEMPERATURE)
    structured_router_llm = llm.with_structured_output(RouterOutput)
    output = structured_router_llm.invoke(messages)
    return {"router_response": output}