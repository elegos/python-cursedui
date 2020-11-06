import curses
from time import sleep

from cursedui import Canvas, CursedUI, Split, Subject, Tile


class Dumb(Tile[str]):
    def render(self, canvas: Canvas) -> None:
        lines = [self.subject * canvas.width for _ in range(canvas.height)]
        canvas.lines = lines

        return canvas


def cursedUIDemo():
    subject1 = Subject('foo ')
    subject2 = Subject('bar ')
    subject3 = Subject('baz ')

    ui = CursedUI(
        Split(
            Dumb(subject1, title='Foo', bordered=True),
            Dumb(subject2, title='Bar', bordered=True),
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


try:
    cursedUIDemo()
    # curses.wrapper(demoFlip)
except Exception as e:
    print(e)
finally:
    curses.curs_set(1)
