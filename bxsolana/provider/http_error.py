from typing import List, Dict, Any

import aiohttp
import betterproto


class HttpError(Exception):
    code: int
    message: str
    details: List[str]

    def __init__(self, code: int, message: str, details: List[str]):
        super().__init__()

        self.code = code
        self.message = message
        self.details = details

    def __str__(self):
        return f"HttpError[{self.code}]: {self.message} ({self.details})"

    @classmethod
    def from_json(cls, payload: Dict[str, Any]) -> "HttpError":
        return cls(
            payload["code"],
            payload["message"],
            payload["details"],
        )


async def map_response(
    response: aiohttp.ClientResponse, destination: betterproto.Message
):
    if response.status != 200:
        response_text = await response.text()
        raise HttpError(code=response.status, message=response_text, details=[])
    response_json = await response.json()
    try:
        http_error = HttpError.from_json(response_json)
        raise http_error
    except KeyError:
        return destination.from_dict(response_json)
