from fastapi import FastAPI, WebSocket
from workflow import workflow
import json

app = FastAPI()

@app.post("/start-process")
async def start_process(data: dict):
    """Entry point for Angular form submission"""
    initial_state = {
        "business_id": data["businessId"],
        "user_input": data["formData"]
    }
    result = workflow.invoke(initial_state)
    return result