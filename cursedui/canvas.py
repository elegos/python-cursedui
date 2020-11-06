import curses
from typing import List

from cursedui.memento import Memento


class Canvas:
    height: int
    width: int

    def __init__(self, height: int, width: int):
        self._lines = Memento([' ' * width for _ in range(height)])
        self.height = height
        self.width = width
        self._pristine = True

    def __setattr__(self, name: str, value) -> None:
        if name not in ['width', 'height']:
            super().__setattr__(name, value)
            return

        # height / width
        lines = self._lines.currentState
        linesLen = len(lines)
        if name == 'height':
            if hasattr(self, 'height') and self.height == value:
                return

            super().__setattr__('height', value)
            self._lines.setState(
                lines[0:value] + [' '*self.width for _ in range(value - linesLen)],
                saveCurrentState=hasattr(self, '_pristine') and self._pristine
            )

        if name == 'width':
            if hasattr(self, 'width') and self.width == value:
                return

            super().__setattr__('width', value)

            self._lines.setState(
                [line[0:value] + ' ' * (value - len(line)) for line in lines],
                saveCurrentState=hasattr(self, '_pristine') and self._pristine,
            )

        self._pristine = False

    @property
    def pristine(self) -> bool:
        return self._pristine

    @property
    def lines(self) -> List[str]:
        return self._lines.currentState

    @lines.setter
    def lines(self, lines: List[str]) -> None:
        if self._lines._state == lines:
            return

        self._lines.setState(lines[0:self.height], saveCurrentState=self._pristine)
        self._pristine = False

    def draw(self, startY: int, startX: int, inner: 'Canvas') -> None:
        '''
        Draw the given canvas at the given coordinates
        '''

        rawLines = self.lines
        for y, line in enumerate(inner.lines):
            rawLine = rawLines[startY + y]
            rawLines[startY + y] = (
                rawLine[:startX - 1 if startX > 1 else 0]
                + line
                + rawLine[startX + len(line):]
            )[0:self.width]

        self.lines = rawLines

    def print(self, window, force: bool = False) -> None:
        '''
        Write the canvas on the given curses window

        :param window: curses window or pad to write on
        :param force: if True, ignore pristine state
        '''

        if self._pristine and not force:
            return

        _, maxX = window.getmaxyx()
        for y, line in enumerate(self._lines.currentState):
            try:
                window.addnstr(y, 0, line, maxX)
            except curses.error:
                pass
        window.refresh()
        self._pristine = True
