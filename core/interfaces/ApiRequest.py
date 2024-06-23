from typing import Any

class ApiRequest:

    def __init__(self) -> None:
        pass

    def __call__(self) -> dict[str, Any] | list[Any] | str | int | float | bool:
        return ""