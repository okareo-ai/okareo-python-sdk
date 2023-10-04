import typing
from datetime import datetime
from typing import TypedDict

import httpx

from .common import BASE_URL


class Generation(TypedDict):
    id: str
    data: datetime


class Okareo:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_generations(self) -> typing.Any:
        r = httpx.get(f"{BASE_URL}/v0/generations", headers={"Api-Key": self.api_key})
        try:
            r.raise_for_status()
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
        return r.json()
