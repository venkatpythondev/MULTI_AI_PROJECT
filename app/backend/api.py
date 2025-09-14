from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from app.common.custom_exception import CustomException
from app.core.ai_agent import get_response_from_ai_agents
from app.common.logger import get_logger
from app.config.settings import settings

logger = get_logger(__name__)
app=FastAPI(title="MULTI-AI AGENT")

class Requeststate(BaseModel):
    model_name:str
    system_prompt:str
    messages:List[str]
    allow_search:bool

@app.post("/chat")
def chat_endpoint(request:Requeststate):
        logger.info(f"Received request with model: {request.model_name}")
        if request.model_name not in settings.ALLOWED_MODELS:
            logger.warning(f"Invalid model name.")
            raise HTTPException(status_code=400, detail="Invalid model name")
        try:
            response = get_response_from_ai_agents(
                request.model_name,
                request.messages,
                request.allow_search,
                request.system_prompt
            )
            logger.info(f"Sucesfully got response from AI Agent {request.model_name}")
            return {"response": response}
        
        except Exception as e:
            logger.error(f"Some error ocuured during reponse generation")
            raise HTTPException(
                 status_code=500,
                 detail=CustomException("Error in AI Agent response generation", error_detail=e)
            )
        
    
