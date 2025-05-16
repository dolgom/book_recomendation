import json
from pathlib import Path
from typing import List, Dict, Any


def load_json(file_path: str) -> List[Dict[str, Any]]:
    """JSON 파일을 로드합니다."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: List[Dict[str, Any]], file_path: str) -> None:
    """데이터를 JSON 파일로 저장합니다."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
