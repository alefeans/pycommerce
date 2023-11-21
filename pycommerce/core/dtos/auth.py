from dataclasses import dataclass


@dataclass
class TokenResponse:
    expire: float
    access_token: str
    token_type: str = "bearer"
