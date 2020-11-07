from typing import Optional

from cursedui import Canvas, Subject, Tile
from cursedui.memento import Memento


class Text(Tile[str]):
    def __init__(
        self,
        subject: Subject[str],
        title: Optional[str] = None,
        bordered: bool = False
    ):
        super(Text, self).__init__(subject=subject, title=title, bordered=bordered)
        self._offsetY = Memento(0)
        self._offsetX = Memento(0)
        self._offsetPristine = False

        self.offsetY = 0
        self.offsetX = 0

    @property
    def offsetY(self) -> int:
        return self._offsetY.currentState

    @offsetY.setter
    def offsetY(self, value: int) -> None:
        maxRenderedLines = self.canvas.height
        maxOffset = len(self.subject.split('\n')) - maxRenderedLines

        if value > maxOffset:
            value = maxOffset

        self._offsetY.setState(value)
        self._offsetPristine = self._offsetPristine and self._offsetY.previousState == value

    @property
    def offsetX(self) -> int:
        return self._offsetX.currentState

    @offsetX.setter
    def offsetX(self, value: int) -> None:
        maxLineLen = max([len(line) for line in self.subject.split('\n')])
        maxRenderedWidth = self.canvas.width
        maxOffset = maxLineLen - maxRenderedWidth

        if maxOffset < 0:
            value = 0
        elif value > maxOffset:
            value = maxOffset

        self._offsetX.setState(value)
        self._offsetPristine = self._offsetPristine and self._offsetX.previousState == value

    def shouldRender(self) -> bool:
        return super(Text, self).shouldRender() or not self._offsetPristine

    def render(self, canvas: Canvas) -> None:
        # Ensure that if the canvas has changed its size, the offset values are still correct
        self.offsetX = self.offsetX
        self.offsetY = self.offsetY

        drawedLines = self.subject.split('\n')[self.offsetY:]
        drawedLines = [line[self.offsetX:] for line in drawedLines]

        canvas.lines = drawedLines
        self._offsetPristine = True
