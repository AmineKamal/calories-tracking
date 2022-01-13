from typing import Any, Dict, List, cast
from src.database.core import DatabaseNode

def to_json(data: Any) -> Any:
    if isinstance(data, DatabaseNode):
        return to_json(data.serialize())
    elif isinstance(data, list):
        return [to_json(e) for e in cast(List[Any], data)]
    elif isinstance(data, dict):
        return {k: to_json(v) for k, v in cast(Dict[str, Any], data.items())}
    else:
        return data