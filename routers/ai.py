from fastapi import APIRouter

from models.ai import PromptRequest
from services.ai_recommendations import (
    parse_user_prompt,
    get_ai_recommendations,
)

router = APIRouter(prefix="/ai",tags=["AI"])

@router.post("/parse")
def ai_parse(request: PromptRequest):
    return parse_user_prompt(request.prompt)

@router.post("/recommendations")
def ai_recommendations(request: PromptRequest):
    return get_ai_recommendations(request.prompt)