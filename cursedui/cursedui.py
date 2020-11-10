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
            curHeight = 0
            for i, tile in enumerate(self.tiles):
                tileHeight = canvasHeight
                tileWidth = width
                # Support for fixed_height tile decorator
                if hasattr(tile, 'fixedHeight'):
                    tileHeight = min(height - curHeight, tile.fixedHeight)
                    canvasHeight = math.floor(
                        (height - curHeight - tileHeight) / (len(self.tiles) - i - 1)
                    )

                # Support for fixed_width tile decorator
                if hasattr(tile, 'fixedWidth'):
                    tileWidth = tile.fixedWidth if tile.fixedWidth <= width else width
                elif hasattr(tile, 'percentWidth'):
                    newWidth = math.floor(width / 100 * tile.percentWidth)
                    tileWidth = newWidth if newWidth <= width else width

                # Fixed height tiles ate all the available vertical space
                if tileHeight <= 1:
                    continue

                tileWindow = curses.newwin(tileHeight, tileWidth, curHeight, 0)
                tile.refresh(tileWindow)
                curHeight += tileHeight

            self._sleepUntilNextFrame(beforeRender)

    def _sleepUntilNextFrame(self, beforeRender: datetime) -> None:
        now = datetime.datetime.now()
        nextFrameDatetime = beforeRender + datetime.timedelta(seconds=self._framePeriod)
        secondsToSleep = (nextFrameDatetime - now).total_seconds()
        if secondsToSleep < 0:
            return

        time.sleep(secondsToSleep)
