from cursedui import Tile
from typing import Callable


def fixed_height(maxHeight: int) -> Callable[[Tile], Tile]:
    '''
    Attempt to allocate exacly the provided height to the tile.
    It might fail if there is no enough space

    :param maxHeight: the desired height
    '''
    def decorator(tile: Tile):
        setattr(tile, 'fixedHeight', maxHeight)

        return tile

    return decorator
