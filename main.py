import pyxel

from pyxelgui import Widget
from pyxelgui import PyxelGui
from pyxelgui import Window
from pyxelgui import Image
from pyxelgui import Text
from pyxelgui import Button

pyxel.init(256,256)
gui = PyxelGui(pyxel_ref=pyxel)

window = Window()
window.x = 20
window.y = 20
window.w = 100
window.h = 50
def update_window(sender):
    sender.x += 1
    text.text = f'window:{window.x}'
window.on_update = update_window
gui.append(widget=window)

text = Text('test')
window.append(widget=text)

button = Button('CLICK')
button.x = 10
button.y = 30
window.append(widget=button)

def update():
    gui.update()

def draw():
    gui.draw()

if __name__ == '__main__':
    print('Start Python GUI test')
    pyxel.run(update=update, draw=draw)
