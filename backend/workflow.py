from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional, List
import logging
from api_ninja import APINinjaClient
from postgres_client import PostgresManager
from form_automation import FormAutomator

class AgentState(TypedDict):
    business_id: str
    user_input: dict
    db_data: Optional[dict]
    api_data: Optional[dict]
    form_data: Optional[dict]
    confirmation: Optional[str]
    errors: List[str]
    retries: int

def collect_input_node(state):
    return {"user_input": state["user_input"]}

def fetch_owner_info_node(state):
    try:
        db = PostgresManager()
        data = db.get_business_data(state["business_id"])
        return {"db_data": data}
    except Exception as e:
        return {"errors": [f"Database error: {str(e)}"]}

def validate_address_node(state):
    client = APINinjaClient()
    address_data = client.get_address_validation(
        state["user_input"]["address"]
    )
    return {"api_data": {"address": address_data[0]}}

def get_demographics_node(state):
    client = APINinjaClient()
    zip_code = state["api_data"]["address"]["zip_code"]
    demographics = client.get_demographics(zip_code)
    return {"api_data": {**state["api_data"], "demographics": demographics}}

def classify_business_node(state):
    try:
        client = APINinjaClient()
        description = state["user_input"]["business_description"]
        naics = client.get_naics_classification(description)
        if not naics:
            raise ValueError("No NAICS classification found")
        return {"api_data": {**state["api_data"], "naics": naics[0]}}
    except Exception as e:
        return {"errors": state.get("errors", []) + [str(e)]}

def prepare_form_data_node(state):
    mapping = {
        "Legal Business Name": state["db_data"]["legal_name"],
        "NAICS Code": state["api_data"]["naics"]["code"],
        "Street Address": state["api_data"]["address"]["street"],
    }
    return {"form_data": mapping}

def submit_form_node(state):
    try:
        automator = FormAutomator()
        confirmation = automator.submit_form(
            "https://business.gov.example/registration",
            state["form_data"]
        )
        return {"confirmation": confirmation}
    except Exception as e:
        return {"errors": state.get("errors", []) + [str(e)]}

def error_handler_node(state):
    if state.get("retries", 0) > 3:
        logging.error("Max retries exceeded")
        return {"errors": state["errors"] + ["Max retries exceeded"]}
    
    return {"retries": state.get("retries", 0) + 1}

def should_retry(state):
    return len(state.get("errors", [])) > 0 and state.get("retries", 0) <= 3

builder = StateGraph(AgentState)

builder.add_node("collect_input", collect_input_node)
builder.add_node("fetch_owner_info", fetch_owner_info_node)
builder.add_node("validate_address", validate_address_node)
builder.add_node("get_demographics", get_demographics_node)
builder.add_node("classify_business", classify_business_node)
builder.add_node("prepare_form_data", prepare_form_data_node)
builder.add_node("submit_form", submit_form_node)
builder.add_node("handle_errors", error_handler_node)

builder.set_entry_point("collect_input")
builder.add_edge("collect_input", "fetch_owner_info")
builder.add_edge("fetch_owner_info", "validate_address")
builder.add_edge("validate_address", "get_demographics")
builder.add_edge("get_demographics", "classify_business")
builder.add_edge("classify_business", "prepare_form_data")
builder.add_edge("prepare_form_data", "submit_form")

builder.add_edge("submit_form", "handle_errors")
builder.add_conditional_edges(
    "handle_errors",
    should_retry,
    {
        True: "validate_address",  
        False: END
    }
)

workflow = builder.compile()