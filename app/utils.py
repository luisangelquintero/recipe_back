import re
import json
import os
from datetime import datetime


def sanitize_filename(text: str) -> str:
    """Convert text to lowercase, replace spaces, remove special characters."""
    text = text.lower().replace(" ", "_")
    text = re.sub(r"[^a-z0-9_\-]", "", text)
    return text
