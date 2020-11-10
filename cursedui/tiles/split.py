import math
from functools import reduce
from math import floor
from typing import List

from cursedui import Canvas, Subject, Tile


class Split(Tile):
    tiles: List[Tile]

    def __init__(self, *tiles: List[Tile]):
        super(Split, self).__init__(subject=Subject(None), title=None, bordered=False)
        self.tiles = tiles

    def render(self, canvas: Canvas) -> None:
        pass

    def onBeforeWindowRefresh(self, window, canvas: Canvas) -> bool:
        numTiles = len(self.tiles)
        tileHeight, splitWidth = window.getmaxyx()
        itemWidth = floor(splitWidth / numTiles)

        currentX = 0
        for i, tile in enumerate(self.tiles):
            tileWidth = itemWidth
            availableSpace = splitWidth - currentX

            # Support for fixed_width tile decorator
            if hasattr(tile, 'fixedWidth'):
                tileWidth = tile.fixedWidth if tile.fixedWidth <= tileWidth else tileWidth
            elif hasattr(tile, 'percentWidth'):
                newWidth = math.floor(splitWidth / 100 * tile.percentWidth)
                tileWidth = newWidth if newWidth <= availableSpace else availableSpace

            tileWindow = window.derwin(tileHeight, tileWidth, 0, currentX)
            tile.refresh(tileWindow)
            currentX += tileWidth
            itemWidth = math.floor((splitWidth - currentX) / max(numTiles - i - 1, 1))

        return False

    def shouldRender(self) -> bool:
        return reduce(lambda a, b: a or b, [tile.shouldRender() for tile in self.tiles], False)
