import os 
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from graph.graph import create_graph
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    graph = create_graph()
    
    research_question = "Why is Maringá considered one of the warmest cities in the state of Paraná, Brazil?"
    
    graph.invoke({"research_question": research_question},
                 config={"recursion_limit": 25})
        
    # # Run the graph until the first interruption
    # thread = {"configurable": {"thread_id": "1"}, "recursion_limit": 15}
    # for event in graph.stream({"research_question": research_question}, 
    #                         thread, 
    #                         stream_mode="updates"):
        
    #     plan = event.get("planner", '')
    #     if plan:
    #         print("PLANNER")
    #         print(f"Search Term: {plan['planner_response'].search_term}")
    #         print(f"Overall Strategy: {plan['planner_response'].overall_strategy}")
    #         print(f"Additional Information: {plan['planner_response'].additional_information}")
    #         print("-" * 50, "\n")
            
    #     web_search = event.get("websearch", '')
    #     if web_search:
    #         print("WEBSEARCH")
    #         print(f"Serper Response: {web_search['serper_response']}")
    #         print("-" * 50, "\n")
        
    #     selected = event.get("selector", "")
    #     if selected:
    #         print("SELECTOR")
    #         print(f"Selected Page Url: {selected['selector_response'].selected_page_url}")
    #         print(f"Description: {selected['selector_response'].description}")
    #         print(f"Reason For Selection: {selected['selector_response'].reason_for_selection}")
    #         print("-" * 50, "\n")
            
    #     scrap = event.get("scrape_website", '')
    #     if scrap:
    #         print("SCRAPER")
    #         print(f"Scraper Response: {scrap['scraper_response'][-1].content}")
    #         print("-" * 50, "\n")
            
    #     report = event.get("reporter", "")
    #     if report:
    #         print("REPORTER")
    #         print(f"Reporter Response: {report['reporter_response'].content}")
    #         print("-" * 50, "\n")
            
    #     review = event.get("reviewer", "")
    #     if review:
    #         print("REVIEWER")
    #         print(f"Feedback: {review['reviewer_response'].feedback}")
    #         print(f"Pass Review: {review['reviewer_response'].pass_review}")
    #         print(f"Comprehensive: {review['reviewer_response'].comprehensive}")
    #         print(f"Citations Provided: {review['reviewer_response'].citations_provided}")
    #         print(f"Relevant to Research Question: {review['reviewer_response'].relevant_to_research_question}")
    #         print("-" * 50, "\n")
            
    #     route = event.get("router", "")
    #     if route:
    #         print("ROUTER")
    #         print(f"Next Agent: {route['router_response'].next_agent}")
    #         print("-" * 50, "\n")
        