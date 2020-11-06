import curses
from abc import abstractmethod
from typing import Optional, TypeVar

from cursedui.canvas import Canvas
from cursedui.observer import Observer
from cursedui.observer import ObserverSubject as Subject

# from cursedui.stringutils import escape_ansi

T = TypeVar('T')


class Tile(Observer[T]):
    title: Optional[str]
    bordered: bool
    subject: T
    canvas: Canvas

    def __init__(
        self,
        subject: Subject[T],
        title: Optional[str] = None,
        bordered: bool = False
    ):
        self.subject = subject.value
        self.title = title
        self.bordered = bordered

        subject.subscribe(self)
        self.canvas = Canvas(0, 0)
        self._subjectPristine = False

    def update(self, subject: T) -> None:
        if subject == self.subject:
            return

        self.subject = subject
        self._subjectPristine = False

    def refresh(self, window) -> None:
        '''
        :param window: curses window
        '''

        if self.shouldRender():
            height, width = window.getmaxyx()
            startX = 0
            startY = 0

            if self.title is not None:
                height -= 1
                startY = 1
            if self.bordered:
                if self.title:
                    height += 1
                height -= 2
                width -= 2
                startY = 1
                startX = 1

            self.canvas.height = height
            self.canvas.width = width
            canvasWindow = window.derwin(height, width, startY, startX)

            if self.bordered:
                window.border()

            if self.title is not None:
                window.addnstr(0, 3, f'   {self.title}   ', width)

            window.refresh()

            self.canvas.width = width
            self.canvas.height = height

            self.render(self.canvas)
            self._subjectPristine = True
            if self.onBeforeWindowRefresh(canvasWindow, self.canvas):
                self.canvas.print(canvasWindow)

    def onBeforeWindowRefresh(self, window, canvas: Canvas) -> bool:
        '''
        Method which runs after the canvas has been modified,
        before its contents are beind displayed on the curses window.

        :param window CursesWindow: the available drawing space
        :param canvas Canvas: alias of self.canvas
        :return: if the refresh method should call the canvas' print
        '''
        return True

    def shouldRender(self) -> bool:
        '''
        Method to detect whether the tile requires a redrawing.
        '''
        return not (self.canvas.pristine and self._subjectPristine)

    @abstractmethod
    def render(self, canvas: Canvas) -> None:
        '''
        Decorate the given canvas to represent self.subject.
        '''
        pass
