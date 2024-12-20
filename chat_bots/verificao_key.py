from typing import Optional
from pydantic import SecretStr, ValidationError
import os


def get_secret_key(key: str) -> Optional[SecretStr]:
    try:
        value = os.getenv(key)
        return SecretStr(value) if value else None
    except ValidationError:
        return None
