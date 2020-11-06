from math import floor
from typing import List
from functools import reduce

from cursedui import Canvas, Subject, Tile


class Split(Tile):
    tiles: List[Tile]

    def __init__(self, *tiles: List[Tile]):
        super(Split, self).__init__(subject=Subject(None), title=None, bordered=False)
        self.tiles = tiles

    def render(self, canvas: Canvas) -> None:
        pass

    def onBeforeWindowRefresh(self, window, canvas: Canvas) -> bool:
        tileHeight, tileWidth = window.getmaxyx()
        tileWidth = floor(tileWidth / len(self.tiles))

        for i, tile in enumerate(self.tiles):
            tileWindow = window.derwin(tileHeight, tileWidth, 0, tileWidth * i)
            tile.refresh(tileWindow)

        return False

    def shouldRender(self) -> bool:
        return reduce(lambda a, b: a or b, [tile.shouldRender() for tile in self.tiles], False)
