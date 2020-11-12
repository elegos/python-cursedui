from cursedui.tiles.text import Text


class Log(Text):
    def update(self, subject: str) -> None:
        prevSubject = self.subject
        super(Log, self).update(subject)

        prevSample = subject[0:100]
        if not prevSample.startswith(prevSubject[0:len(prevSample)]):
            # New log
            self.offsetX = 0
            self.offsetY = 0

        if self.canvas is None:
            return

        height = self.canvas.height

        prevNumLines = len(prevSubject.split('\n'))
        prevExpectedOffset = prevNumLines - height
        if prevExpectedOffset < 0:
            prevExpectedOffset = 0
        numLines = len(subject.split('\n'))
        # If the log was detached, do not scroll down
        if prevExpectedOffset != self.offsetY:
            return

        # Scroll down
        self.offsetY = numLines - height
