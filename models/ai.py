
from pydantic import BaseModel, Field, field_validator

class PromptRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=500)

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Prompt cannot be empty")

        return value