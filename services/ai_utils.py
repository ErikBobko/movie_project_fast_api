from typing import Any
import json


def safe_json_loads(text: str) -> Any:
    """
    Parse a JSON response and tolerate accidental Markdown code fences.
    """
    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```json").removeprefix("```")
        cleaned = cleaned.removesuffix("```").strip()

    return json.loads(cleaned)