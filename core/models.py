from dataclasses import dataclass
from typing import Optional

@dataclass
class Parameter:
    name: str
    location: str
    required: bool
    schema: dict

@dataclass
class Response:
    status_code: int
    description: str
    schema: dict

@dataclass
class Endpoint:
    tag: str
    method: str
    path: str
    parameters: list[Parameter]
    responses: list[Response]
    request_body: Optional[dict] = None
    summary: Optional[str] = None