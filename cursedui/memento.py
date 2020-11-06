from copy import deepcopy
from typing import Generic, TypeVar

T = TypeVar('T')


class Memento(Generic[T]):
    def __init__(self, value: T) -> None:
        self._previous = deepcopy(value)
        self._state = deepcopy(value)

    @property
    def currentState(self) -> T:
        return deepcopy(self._state)

    @property
    def previousState(self) -> T:
        return deepcopy(self._previous)

    def setState(self, value: T, saveCurrentState: bool = True) -> None:
        if saveCurrentState:
            self._previous = deepcopy(self._state)

        self._state = value
