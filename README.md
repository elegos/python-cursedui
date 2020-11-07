# CursedUI

[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
![PyPI](https://img.shields.io/pypi/v/cursedui)
![PyPI - Status](https://img.shields.io/pypi/status/cursedui)

This is a python graphic library based on the curses library.

It hides the complexity of the basic library and offers a class-first approach to UI.

## Example usage

See [example.py](example.py).

You can run the example simply by running `python example.py`.

## Available tiles

### [Split](cursedui/tiles/split.py)

Equally vertically splits the available space between its child tiles.


```python
from cursedui import Split

splitTile = Split(tile1, tile2, ...)
```

### [Text](cursedui/tiles/text.py)

Shows the string subject in the available canvas. `offsetX` and `offsetY` attributes allow to move the pane of the visible text.

Invalid offset values will be reset either to 0 (if offset &lt; 0) or to the calculated maximum offset (if offset &gt; maximum offset).

```python
from cursedui import Text

textSubject = Subject('myText')
splitTile = Text(title='My title', bordered=True, subject=textSubject)

splitTile.offsetY = 27 # might default to the maximum possible offset
splitTile.offsetX = -1 # defaults to 0
```

## Extending (creating new tiles)

The library is made to be easily enhanced with new tiles.

To create a new tile, you need to extend the `cursedui.Tile` class and implement its abstract `render` method.

See the [tile.py](cursedui/tile.py) file to see the rest of the overrideable methods.

See [tiles](cursedui/tiles) folder for a list of tiles available out-of-the-box.

Other than the `render` method, you might want to override the following methods:

- `Tile.onBeforeWindowRefresh` - used to access the curses' window (it should be used for particular cases only). See the [Split tile](cursedui/tiles/split.py) for an example.
- `Tile.shouldRender` - which should be overwritten returning the super's result and the new tile's particular logic. See the [Text tile](cursedui/tiles/text.py) for an example.

```python
from typing import List

from cursedui import Tile, Subject


class Dumb(Tile[str]):
    def render(self, canvas: Canvas) -> None:
        lines = [self.subject * canvas.width for _ in range(canvas.height)]
        canvas.lines = lines

        return canvas
```
