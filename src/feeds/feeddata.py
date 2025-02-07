from dataclasses import dataclass
from typing import Callable


@dataclass
class FeedData :
    shortname : str
    filter : Callable[[str, dict], bool]
    get_posts : Callable