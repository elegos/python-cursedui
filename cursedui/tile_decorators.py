from cursedui import Tile
from cursedui.exceptions import DecoratorException
from typing import Callable, Optional


def fixed_height(maxHeight: int) -> Callable[[Tile], Tile]:
    '''
    Attempt to allocate exacly the provided height to the tile.
    It might fail if there is no enough space.

    Works on top-level tiles only (direct children of CursedUI).

    :param maxHeight: the desired height
    '''
    def decorator(tile: Tile) -> Tile:
        setattr(tile, 'fixedHeight', maxHeight)

        return tile

    return decorator


def fixed_width(
    maxWidth: Optional[int] = None,
    maxWidthPercent: Optional[int] = None,
) -> Callable[[Tile], Tile]:
    '''
    Attempt to allocate exactly the provided width to the tile.
    Either maxWidth or maxWidthPercent must be set. If both are set, maxWidth will be taken.

    Works on top-level and Split tiles (direct children of CursedUI and Split tile)

    :param maxWidth: absolute width
    :param maxWidthPercent: % width (0-100)
    '''

    if maxWidthPercent is not None:
        if maxWidthPercent <= 0:
            maxWidthPercent = 1
        elif maxWidthPercent > 100:
            maxWidthPercent = 100

    def decorator(tile: Tile) -> Tile:
        if maxWidth is not None:
            setattr(tile, 'fixedWidth', maxWidth)
        elif maxWidthPercent is not None:
            setattr(tile, 'percentWidth', maxWidthPercent)
        else:
            raise DecoratorException(
                'fixed_width: You have to specify either maxWidth or maxWidthPercent'
            )

        return tile

    return decorator
