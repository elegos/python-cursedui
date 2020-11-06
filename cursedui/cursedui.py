import curses
import datetime
import math
import time
from functools import reduce
from threading import Thread
from typing import List, Optional

from cursedui.canvas import Canvas
from cursedui.memento import Memento
from cursedui.tile import Tile


class CursedUI:
    active: bool
    tiles: List[Tile]
    canvas: Canvas

    def __init__(self, *tiles: Tile, maxRefreshRate: int = 30):
        self.active = False
        self._uiThread: Optional[Thread] = None
        self._framePeriod = 1.0 / maxRefreshRate
        self.tiles = list(tiles)
        self.canvas = Canvas(0, 0)

    def start(self):
        # Already running
        if self.active and self._uiThread is not None and self._uiThread.is_alive():
            return

        self.active = True

        def wrapperRunner():
            try:
                curses.wrapper(self._run)
            except Exception as e:
                print(e)
            finally:
                curses.curs_set(1)

        self._uiThread = Thread(daemon=True, target=wrapperRunner)
        self._uiThread.start()

    def stop(self, synchronous: bool = True):
        self.active = False
        if self._uiThread is not None and self._uiThread.is_alive():
            self._uiThread.join()

    def join(self):
        if self._uiThread is not None and self._uiThread.is_alive():
            self._uiThread.join()

    def _run(self, stdscr):
        stdscr.clear()
        curses.curs_set(0)
        self._state = Memento([])

        while self.active:
            beforeRender = datetime.datetime.now()

            height, width = stdscr.getmaxyx()
            if (
                self.canvas.height == height
                and self.canvas.width == width
                and not reduce(lambda x, y: x or y, [
                    tile.shouldRender(width, height)
                    for tile in self.tiles
                ], False)
            ):
                self._sleepUntilNextFrame(beforeRender)
                continue

            # Render
            canvasHeight = math.floor(height / len(self.tiles))
            for i, tile in enumerate(self.tiles):
                tileWindow = curses.newwin(canvasHeight, width, canvasHeight * i, 0)
                tile.refresh(tileWindow)

            self._sleepUntilNextFrame(beforeRender)

    def _sleepUntilNextFrame(self, beforeRender: datetime) -> None:
        now = datetime.datetime.now()
        nextFrameDatetime = beforeRender + datetime.timedelta(seconds=self._framePeriod)
        secondsToSleep = (nextFrameDatetime - now).total_seconds()
        if secondsToSleep < 0:
            return

        time.sleep(secondsToSleep)
