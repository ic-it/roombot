from typing import Any


class IDatabase:
    def connect(self): ...
    def execute(self, *args, **kwargs) -> Any: ...
    def commit(self): ...
    def close(self): ...

