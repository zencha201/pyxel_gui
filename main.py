import pyxel
from pyxelgui import PyxelGui
from pyxelgui import Window
from pyxelgui import Image
from pyxelgui import Text
from pyxelgui import Button

# Pyxel初期化
pyxel.init(256,256)
# PyxelGUI初期化
gui = PyxelGui(pyxel_ref=pyxel)

# ウィジェット生成
window = Window('MAIN WINDOW', 20, 20, 100, 50)
gui.append(widget=window)

count = 0
text = Text('test', 5, 15, color=pyxel.COLOR_BLACK)
window.append(widget=text)

button = Button('CLICK', 10, 30)
def on_mouse_click_button(self, btn):
    global count
    count += 1
    text.text = f'{count}'
    text.color = pyxel.COLOR_RED
button.on_click = on_mouse_click_button.__get__(button, Button)
window.append(widget=button)

window2 = Window('MAIN WINDOW2', 20, 100, 100, 100)
def update_window2(self):
    self.x += 0.1
window2.on_update = update_window2.__get__(window2, Window)
gui.append(widget=window2)

image1 = Image(10, 10, 50, 50)
def draw_widget_image1(self):
    base_x = self.get_abs_x()
    base_y = self.get_abs_y()
    pyxel.rect(base_x + 0, base_y + 0, 50, 50, pyxel.COLOR_BROWN)
image1.draw_widget = draw_widget_image1.__get__(image1, Image)
window2.append(widget=image1)

def update():
    '''
    更新処理
    '''
    gui.update()

def draw():
    '''
    描画処理
    '''
    gui.draw()

if __name__ == '__main__':
    print('Start Python GUI test')
    pyxel.run(update=update, draw=draw)
