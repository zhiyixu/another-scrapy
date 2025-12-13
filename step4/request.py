# requests.py
from dataclasses import dataclass
from typing import Callable, Iterable, Union, Optional, Dict, Any


@dataclass
class Request:
    url: str
    callback: Callable[[str], Iterable[Union["Request", dict]]] | Any
    headers: Optional[Dict[str, str]] = None