from typing import Any, List, Callable, Optional


def find(
    array: List[Any], condition: Callable[[Any], bool]
) -> Optional[Any]:
    return next(
        (item for item in array if condition(item)), None
    )


def any_match(
    array: List[Any], condition: Callable[[Any], bool]
) -> bool:  # pragma: no cover
    return any(condition(item) for item in array)


def every(
    array: List[Any], condition: Callable[[Any], bool]
) -> bool:  # pragma: no cover
    return all(condition(item) for item in array)
