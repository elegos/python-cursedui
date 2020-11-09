import curses
from time import sleep

from cursedui import Canvas, CursedUI, Split, Subject, Text, Tile
from cursedui.tile_decorators import fixed_height

# Used for development reasons


class Dumb(Tile[str]):
    def render(self, canvas: Canvas) -> None:
        lines = [self.subject * canvas.width for _ in range(canvas.height)]
        canvas.lines = lines

        return canvas


def cursedUIDemo():
    subject0 = Subject("I'm a fixed-height tile - ")
    subject1 = Subject('foo ')
    subject2 = Subject('bar ')
    subject3 = Subject('baz ')

    ui = CursedUI(
        fixed_height(4)(Dumb(subject0, title='Fixed (4)', bordered=True)),
        fixed_height(20)(Dumb(subject0, title='Fixed (20)', bordered=True)),
        Split(
            Dumb(subject1, title='Foo', bordered=True),
            Dumb(subject2, title=None, bordered=False),
            Dumb(subject3, title='Baz', bordered=True),
        ),
    )

    ui.start()
    for _ in range(25):
        sleep(0.2)

        s1 = subject1.value
        s2 = subject2.value
        s3 = subject3.value

        subject1(s2)
        subject2(s3)
        subject3(s1)

    ui.stop()


def demoFlip(window):
    curses.curs_set(0)
    c = Canvas(10, 19)

    while True:
        c.lines = [
            '1                  ',
            '  2                ',
            '    3              ',
            '      4            ',
            '        5          ',
            '          6        ',
            '            7      ',
            '              8    ',
            '                9  ',
            '                  0',
        ]
        c.print(window)
        window.refresh()
        sleep(1.0/30)
        c.lines = [
            '        1          ',
            '        2          ',
            '        3          ',
            '        4          ',
            '        5          ',
            '        6          ',
            '        7          ',
            '        8          ',
            '        9          ',
            '        0          ',
        ]
        c.print(window)
        window.refresh()
        sleep(1.0/30)

        c.lines = [
            '                  0',
            '                9  ',
            '              8    ',
            '            7      ',
            '          6        ',
            '        5          ',
            '      4            ',
            '    3              ',
            '  2                ',
            '1                  ',
        ]
        c.print(window)
        window.refresh()
        sleep(1.0/30)

        c.lines = [
            '                   ',
            '                   ',
            '                   ',
            '                   ',
            '1 2 3 4 5 6 7 8 9 0',
            '                   ',
            '                   ',
            '                   ',
            '                   ',
            '                   ',
        ]
        c.print(window)
        window.refresh()
        sleep(1.0/30)


def textTileDemo():
    # flake8: noqa E501
    subject = Subject('''Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Aenean eget ipsum luctus, scelerisque lorem a, tempus augue.
Ut blandit eleifend dolor ac tristique.
Curabitur in lectus a eros suscipit fringilla non non ipsum.
Proin lorem turpis, tempor vel leo nec, sodales laoreet dolor.
Cras ultrices sagittis mollis. Sed efficitur eros purus, ac convallis magna iaculis id.
Praesent quis neque sed tellus tincidunt consequat et in massa. Nullam et dictum orci.
Nunc varius dolor eget imperdiet molestie. Nam nec est eleifend, facilisis diam et, varius orci.
Phasellus dui mi, pharetra at ligula eu, euismod consectetur quam.
Integer congue tortor augue, quis ultrices risus dictum et.
Fusce dignissim hendrerit turpis vel semper.
Fusce accumsan dolor at vehicula venenatis.

Donec mattis ipsum eget elit bibendum, molestie malesuada massa laoreet. Praesent ut felis interdum, molestie mauris at, sagittis nisl.
Pellentesque porta, augue molestie finibus aliquet, lectus lectus pulvinar ex, ut mattis libero lacus in lorem. In a fermentum ex.
Suspendisse finibus nunc vulputate erat posuere pretium. Praesent sagittis sapien eget molestie bibendum.
Vivamus id pellentesque est, vitae imperdiet velit. Nullam nec massa lectus.
Quisque semper tempus molestie. Sed laoreet, sapien sit amet cursus ullamcorper, odio enim pulvinar tortor, lobortis pulvinar ex augue venenatis felis.
Fusce egestas, quam quis malesuada vestibulum, elit est tristique lacus, sed molestie mauris ex vel leo.

Mauris sapien massa, blandit id pulvinar at, euismod vel nibh. Nulla sit amet efficitur lacus. Suspendisse varius pharetra nisl vel viverra.
Aliquam aliquet at tortor ut tincidunt. Nunc a gravida nunc. Aenean ante elit, congue in consequat ac, porta sed arcu.
Lorem ipsum dolor sit amet, consectetur adipiscing elit.

In hac habitasse platea dictumst. Vivamus varius sapien a orci auctor luctus. Donec sed urna ipsum. Vestibulum nulla neque, pretium at ipsum vel, efficitur molestie orci.
Nullam ac lacinia magna, ut ultrices enim. Nunc aliquam nisl purus, vel convallis purus porta eget. Morbi a metus orci. Proin mauris nunc, elementum ac egestas eu, blandit sit amet mi.
Nullam placerat ut nibh eget volutpat. Sed velit magna, consectetur eget pharetra vel, auctor et erat. Aenean vel iaculis tellus. Integer feugiat ante velit, ut efficitur nisi condimentum sed.''')

    textTile = Text(subject=subject, title='Text tile', bordered=True)
    ui = CursedUI(textTile)

    ui.start()

    for offset in range(20):
        textTile.offsetY = offset
        sleep(0.25)

    for offset in range(20):
        textTile.offsetX = offset
        sleep(0.25)

    sleep(3)
    ui.stop()


try:
    # textTileDemo()
    cursedUIDemo()
    # curses.wrapper(demoFlip)
except Exception as e:
    print(e)
finally:
    curses.curs_set(1)
