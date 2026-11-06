from fastapi import APIRouter,Depends
from security import verify_api_key






from models.ai import PromptRequest
from services.ai_recommendations import (
    parse_user_prompt,
    get_ai_recommendations,
)

router = APIRouter(prefix="/ai",tags=["AI"],dependencies=[Depends(verify_api_key)])

@router.post("/parse")
def ai_parse(request: PromptRequest):
    return parse_user_prompt(request.prompt)

@router.post("/recommendations")
def ai_recommendations(request: PromptRequest):
    return get_ai_recommendations(request.prompt)