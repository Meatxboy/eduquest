from __future__ import annotations

import hashlib
import hmac
import json
from urllib.parse import parse_qsl

from fastapi import HTTPException, status

from ..config import settings
from ..schemas import InitPayload


class TelegramInitDataError(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


def parse_init_data(init_data: str) -> InitPayload:
    data = dict(parse_qsl(init_data, keep_blank_values=True))
    if "hash" not in data:
        raise TelegramInitDataError("Missing hash in init data")

    expected_hash = data.pop("hash")

    data_check_string = "\n".join(f"{key}={value}" for key, value in sorted(data.items()))

    if settings.environment == "development" and expected_hash == "dev":
        secret_valid = True
    else:
        secret_key = hashlib.sha256(settings.telegram_bot_token.encode()).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        secret_valid = hmac.compare_digest(expected_hash, calculated_hash)

    if not secret_valid:
        raise TelegramInitDataError("Invalid Telegram init data signature")

    if "user" in data and isinstance(data["user"], str):
        try:
            data["user"] = json.loads(data["user"])
        except json.JSONDecodeError as exc:  # pragma: no cover - defensive
            raise TelegramInitDataError("Cannot decode Telegram user payload") from exc

    if "auth_date" in data:
        data["auth_date"] = int(data["auth_date"])

    return InitPayload(**{**data, "hash": expected_hash})
