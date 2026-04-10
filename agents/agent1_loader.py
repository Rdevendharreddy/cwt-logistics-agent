import os
from pathlib import Path
from typing import List


def load_pdfs(data_dir: str = 'data') -> List[str]:
    """Load PDF file paths from the configured data directory."""
    path = Path(data_dir)
    if not path.exists() or not path.is_dir():
        return []

    pdf_files = [str(item.resolve()) for item in path.iterdir() if item.is_file() and item.suffix.lower() == '.pdf']
    return sorted(pdf_files)
