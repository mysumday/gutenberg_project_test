from typing import TypeVar
import re
from pathlib import Path

T = TypeVar("T")
def get_by_part_key(d: dict[str, T], k: str, /) -> T | None:
    """Retrieve the value from a dictionary where the key contains a given substring."""
    for key, value in d.items():
        if k in key:
            return value


def normalize(text: str, /) -> str:
    """Normalize a string by converting it to lowercase and replacing spaces/commas with underscores."""
    return re.sub(r'[,\s]+', '_', text.strip().lower())

def get_auth_from_dir(root_dir: Path, /) -> list[str]:
    """Get a list of normalized author directory names from a given root directory."""
    return [
        normalize(author.name)
        for author in root_dir.iterdir()
        if author.is_dir()
    ]
    
def chunk_text(text, chunk_size=500, overlap=100):
    "Split input text into chunks of tokens with optional overlap."
    tokens = text.split()
    chunks = []
    for i in range(0, len(tokens), chunk_size - overlap):
        chunk = ' '.join(tokens[i:i+chunk_size])
        chunks.append(chunk)
    return chunks