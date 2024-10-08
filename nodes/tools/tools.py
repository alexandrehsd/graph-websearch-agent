import os 
import requests
import json
from states.states import AgentGraphState
from bs4 import BeautifulSoup
from langchain_core.messages import SystemMessage
from nodes.tools.utils import format_results, is_garbled


def google_serper(state: AgentGraphState):
    
    search_term = state["planner_response"].search_term
    search_url = "https://google.serper.dev/search"
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': os.environ["SERPER_API_KEY"]
    }
    payload = json.dumps({"q": search_term})
    
    try:
        response = requests.post(search_url, headers=headers, data=payload)
        response.raise_for_status()
        results = response.json()
        
        if 'organic' in results:
            formatted_results = format_results(results["organic"])
            return {"serper_response": formatted_results}
        else:
            return {"serper_response": "No organic results found"}
    
    except requests.exceptions.HTTPError as http_error:
        return {**state, "serper_response": f"HTTP error occurred: {http_error}"}
    except requests.exceptions.RequestException as req_error:
        return {**state, "serper_response": f"Request error occurred: {req_error}"}
    except KeyError as key_error:
        return {**state, "serper_response": f"Key error occurred: {key_error}"}


def scrape_website(state: AgentGraphState):
    selector_response = state.get("selector_response", None)
    
    try:    
        url = selector_response.selected_page_url
    except AttributeError as e:
        return {**state,
                "scraper_response":
                    f"""
                    AttributeError occurred when trying to retrieve page URL: {e}.
                    Make sure `selected_page_url` is not None.
                    """
                }
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")  # parse the html string

        # extract content
        texts = soup.stripped_strings
        content = " ".join(texts)

        if is_garbled(content):
            content = "error in scraping website, garbled text returned."
        else:
            content = content[:4000]  # limit the content to 4000 characters    
    except requests.HTTPError as http_error:
        if http_error.response.status_code == 403:
            content = f"error in scraping website, 403 forbidden for url: {url}"
        else:
            content = f"error in scraping website, {str(e)}"
    except requests.RequestException as req_error:
        content = f"error in scraping website, {str(req_error)}"
    
    state["scraper_response"].append(
            SystemMessage(
                content=str({"source": url, "content": content})
            )
        )
        
    return {"scraper_response": state["scraper_response"]}


def print_report(state: AgentGraphState):
    """Redirect the final report to the END of the graph"""
    final_report = "\n\n".join(report.content for report in state["reporter_response"])
    
    print(f"Final Report 📝:\n\n\n{final_report}")
    return state


def routing(state: AgentGraphState):
    next_agent = state["router_response"].next_agent
    
    if state["reviewer_response"].pass_review == "True":
        return "print_report"
    
    if next_agent in ["planner", "selector", "reporter", "print_report"]:
        return next_agent
    else:
        raise Exception("Router Agent return an Invalid Output.")
