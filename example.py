from cursedui import CursedUI, Split, Subject, Text
from time import sleep


# Subjects are generic-typed observer pattern subjects,
# which can be easily updated by calling themselves.
# Their type depends on the constructor's argument.
# Each tile should specify a non-generic TileSubject.
textSubject1 = Subject('Lorem ipsum dolor sit amet, consectetur adipiscing elit.')
textSubject2 = Subject('Duis erat augue, maximus nec nunc ut, porta interdum elit.')
textSubject3 = Subject('Aenean sit amet turpis convallis, ullamcorper velit at, facilisis nisl.')
textSubject4 = Subject('Curabitur tincidunt elit elit, lacinia molestie enim accumsan ut.')

# CursedUI logics resemble the ones of an HTML document,
# and thus the tiles are block-like elements,
# taking the full width of the (available) view.
ui = CursedUI(
    Text(subject=textSubject1, bordered=False, title='Unbordered text tile'),
    # The Split tile takes other tiles as arguments, producing an equally vertically
    # split view
    Split(
        Text(subject=textSubject2, bordered=True, title='Split 1'),
        Text(subject=textSubject3, bordered=True, title='Split 2'),
        Text(subject=textSubject4, bordered=True, title='Split 3'),
    ),
)

# The UI runs in an asynchronous thread, letting the application's logics
# run in the main thread, simplifying the writing of the main file.
ui.start()

# Application's logics
sleepTime = 1.0
while sleepTime > 0.1:
    sleepTime = sleepTime * 0.9
    text1 = textSubject1.value
    text2 = textSubject2.value
    text3 = textSubject3.value
    text4 = textSubject4.value

    # To update a TileSubject, just call it again with the new content.
    # The UI will refresh only if any of the subjects change, or a tile requires it.
    # The single tiles will refresh their graphic representation only if their subject will change.
    textSubject1(text4)
    textSubject2(text1)
    textSubject3(text2)
    textSubject4(text3)

    sleep(sleepTime)

textSubject1('Freeze!')
textSubject2('Freeze!')
textSubject3('Freeze!')
textSubject4('Freeze!')

sleep(3)

# Stop the UI. It awaits for the UI thread to stop.
ui.stop()
