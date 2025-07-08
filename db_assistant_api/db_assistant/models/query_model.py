from typing_extensions import Annotated
from typing import TypedDict

class QueryOutput(TypedDict):
    query: Annotated[str, ..., "Syntactically valid query"]