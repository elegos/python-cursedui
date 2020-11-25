from cursedui import Canvas, Tile, Subject
from typing import Optional
from math import ceil


class ProgressBar(Tile[int]):
    total: int

    def __init__(
        self,
        total: int,
        subject: Subject[int],
        title: Optional[str] = None,
        bordered: bool = False,
        showNumbers: bool = True,
    ):
        super().__init__(subject, title, bordered)
        self._showNumbers = showNumbers
        self.total = total

    def render(self, canvas: Canvas) -> None:
        current = self.subject if self.subject <= self.total else self.total
        availableSpace = canvas.width - 4
        if self._showNumbers:
            availableSpace -= 2 + len(str(self.total)) * 2

        counter = ''
        if self._showNumbers:
            totalLength = len(str(self.total))
            counter = f'{str(current).zfill(totalLength)}/{self.total} '

        dashesNumber = ceil(availableSpace * current / 100)
        progressLine = '-' * dashesNumber
        progressLine += ' ' * (availableSpace - dashesNumber)

        line = '{}| {} |'.format(counter, progressLine)
        lines = [line]
        lines.extend([' ' * canvas.width for _ in range(canvas.height - 1)])
        canvas.lines = lines
