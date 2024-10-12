# utils.py

import uuid

def generate_unique_suffix(length=8):
    """고유한 식별자를 생성하여 반환합니다."""
    return str(uuid.uuid4())[:length]
