# requests.py
from dataclasses import dataclass
from typing import Callable, Iterable, Union, Optional, Dict


@dataclass
class Request:
    url: str
    callback: Callable[[str], Iterable[Union["Request", dict]]]
    headers: Optional[Dict[str, str]] = None