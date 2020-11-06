from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar
from copy import deepcopy

T = TypeVar('T')


class Observer(Generic[T], ABC):
    @abstractmethod
    def update(self, subject: T) -> None:
        pass


class ObserverSubject(Generic[T]):
    def __init__(self, value: T):
        self._value = value
        self._subscribers: List[Observer[T]] = []

    @property
    def value(self):
        return deepcopy(self._value)

    def subscribe(self, observer: Observer[T]):
        if observer not in self._subscribers:
            self._subscribers.append(observer)

    def unsubscribe(self, observer: Observer[T]):
        if observer in self._subscribers:
            self._subscribers.remove(observer)

    def __call__(self, value: T):
        self._value = value

        # Prevent observers to edit the original value
        value = deepcopy(value)
        for observer in self._subscribers:
            observer.update(value)
