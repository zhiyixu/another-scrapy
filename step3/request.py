# requests.py
from dataclasses import dataclass
from typing import Callable

@dataclass
class Request:
    url: str
    callback: Callable[[str], list]
