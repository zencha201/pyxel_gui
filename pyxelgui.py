if __name__ == '__main__':
    import pyxel
else:
    pyxel = None

_font = None

_FONT_SIZE = 10
_FONT_WIDTH_ASCII = 6
_FONT_WIDTH_2BYTE = 10
_WINDOW_TITLE_BAR_SIZE = _FONT_SIZE + 4
_TEXT_HEIGHT = _FONT_SIZE + 7
_BUTTON_HEIGHT = _TEXT_HEIGHT

class Widget:
    '''
    ウィジェットのベースクラス
    '''
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.enable = True
        self.visible = True
        self.focus = False
        self.own = None
        self.widgets = [] # ウィジェットリスト。Zオーダー奥順
            
    def get_abs_x(self):
        '''
        ウィジェットの絶対X座標を取得する
        '''
        return self.x + self.own.get_abs_x() if self.own != None else 0
    
    def get_abs_y(self):
        '''
        ウィジェットの絶対Y座標を取得する
        '''
        return self.y + self.own.get_abs_y() if self.own != None else 0
    
    def on_focus(self):
        '''
        フォーカスイベントハンドラ
        '''
        self.focus = True
    
    def on_unfocus(self):
        '''
        フォーカス解除イベントハンドラ
        '''
        self.focus = False
    
    def on_key_down(self, key):
        '''
        キーダウンイベントハンドラ
        '''
        pass
    
    def on_key_up(self, key):
        '''
        キーアップイベントハンドラ
        '''
        pass
    
    def on_key_press(self, key):
        '''
        キー押下イベントハンドラ
        '''
        pass
    
    def on_mouse_move(self, x, y):
        '''
        マウス移動イベントハンドラ
        '''
        for widget in self.widgets:
            if widget.x <= x and widget.y <= y and widget.x + widget.w >= x and widget.y + widget.h >= y:
                widget.on_mouse_move(x - widget.x, y - widget.y)
    
    def on_mouse_down(self, btn, x, y):
        '''
        マウスボタンダウンイベントハンドラ
        '''
        for widget in self.widgets:
            if widget.x <= x and widget.y <= y and widget.x + widget.w >= x and widget.y + widget.h >= y:
                widget.on_mouse_down(btn, x - widget.x, y - widget.y)
                widget.on_click(btn)
    
    def on_mouse_up(self, btn, x, y):
        '''
        マウスボタンアップイベントハンドラ
        '''
        for widget in self.widgets:
            if widget.x <= x and widget.y <= y and widget.x + widget.w >= x and widget.y + widget.h >= y:
                widget.on_mouse_up(btn, x - widget.x, y - widget.y)
    
    def on_update(self):
        '''
        更新イベントハンドラ
        '''
        pass
    
    def on_draw(self):
        '''
        描画イベントハンドラ
        '''
        pass
    
    def on_click(self, btn):
        '''
        クリックイベントハンドラ
        '''
        pass
        
    def append(self, widget):
        '''
        ウィジェット追加
        '''
        self.widgets.append(widget)
        widget.own = self
    
    def remove(self, widget):
        '''
        ウィジェット削除
        '''
        self.widgets.remove(widget)
        widget.own = None
    
    def update_widget(self):
        '''
        ウィジェット単体の更新処理
        
        ウィジェットの更新を実装する場合は、本関数内に実装する。
        '''
        pass
    
    def update(self):
        '''
        ウィジェットの更新処理
        
        下記の優先度でウィジェットを更新する
        1. 自身の更新処理
        2. ユーザ定義の更新処理
        3. サブウィジェットの更新処理
        '''
        if self.enable:
            self.update_widget()
            self.on_update()
            for widget in self.widgets:
                widget.update()
    
    def draw_widget(self):
        '''
        ウィジェット単体の描画処理
        
        ウィジェットの描画を実装する場合は、本関数内に実装する。
        '''
        pass
    
    def draw(self):
        '''
        ウィジェットの描画処理
        
        下記の優先度でウィジェットを描画する
        1. 自身の描画処理
        2. ユーザ定義の描画処理
        3. サブウィジェットの描画処理
        '''
        if self.visible:
            # 描画範囲をウイジェットの領域内に限定
            pyxel.clip(self.get_abs_x(), self.get_abs_y(), self.w, self.h)
            
            self.draw_widget()
            self.on_draw()
            for widget in self.widgets:
                widget.draw()
                
            # 描画範囲をリセット
            pyxel.clip()

class PyxelGui(Widget):
    '''
    画面構成上のトップレイヤー
    イベント配送処理は本関数内に実装する
    '''
    def __init__(self, pyxel_ref=None):
        if pyxel_ref != None:
            global pyxel
            pyxel = pyxel_ref
        super().__init__(0, 0, pyxel.width, pyxel.height)
        pyxel.mouse(True)
        
        # フォント処理
        global _font
        _font = pyxel.Font("assets/umplus_j10r.bdf")
        
        # マウスイベント関係
        self.mouse_x = pyxel.mouse_x
        self.mouse_y = pyxel.mouse_y
        self.mouse_btn = {pyxel.MOUSE_BUTTON_LEFT : False, 
                          pyxel.MOUSE_BUTTON_MIDDLE : False, 
                          pyxel.MOUSE_BUTTON_RIGHT : False}
    
    def on_mouse_down(self, btn, x, y):
        '''
        マウスボタンダウンイベントハンドラ
        PyxelGuiのみ、ウィンドウのフォーカス遷移を行うため、独自実装とする
        '''
        for widget in self.widgets[::-1]:
            if widget.x <= x and widget.y <= y and widget.x + widget.w >= x and widget.y + widget.h >= y:
                # 2番目以降のウィンドウの場合、フォーカス切り替え処理を行う
                if self.widgets[-1] != widget: # 2番目以降のウィンドウ
                    self.widgets[-1].on_unfocus()
                    widget.on_focus()
                    self.widgets.remove(widget)
                    self.widgets.append(widget)
                
                widget.on_mouse_down(btn, x - widget.x, y - widget.y)
                widget.on_click(btn)
                break
    
    def detect_mouse_event(self):
        # マウスイベント
        current_mouse_x = pyxel.mouse_x
        current_mouse_y = pyxel.mouse_y
        if self.mouse_x != current_mouse_x or self.mouse_y != current_mouse_y:
            self.on_mouse_move(self.mouse_x, self.mouse_y)
        self.mouse_x = current_mouse_x
        self.mouse_y = current_mouse_y
        
        cureent_mouse_btn = {}
        for key in self.mouse_btn.keys():
            cureent_mouse_btn[key] = pyxel.btn(key)
            if self.mouse_btn[key] != cureent_mouse_btn[key]:
                if cureent_mouse_btn[key]:
                    self.on_mouse_down(key, self.mouse_x, self.mouse_y)
                else:
                    self.on_mouse_up(key, self.mouse_x, self.mouse_y)
            self.mouse_btn[key] = cureent_mouse_btn[key]
        
    def update_widget(self):
        '''
        イベント処理
        '''
        # イベント検出処理 / 配送処理
        self.detect_mouse_event()
        
        # フォーカス処理
        pass
    
    def draw_widget(self):
        pyxel.cls(pyxel.COLOR_GRAY)

class Window(Widget):
    '''
    ウィンドウ
    '''
    def __init__(self, text, x=0, y=0, w=100, h=80, color=0):
        super().__init__(x, y, w, h)
        self.text = text
        self.is_drag = False
        self.drag_start_mouse_x = 0
        self.drag_start_mouse_y = 0
    
    def on_mouse_move(self, x, y):
        '''
        マウス移動イベントハンドラ
        '''
        if self.is_drag:
            pass
        else:
            super().on_mouse_move(x, y)
    
    def on_mouse_down(self, btn, x, y):
        '''
        マウスボタンダウンイベントハンドラ
        '''
        # タイトルバーがある場合、ドラッグモード判定
        if len(self.text) > 0 and y < _WINDOW_TITLE_BAR_SIZE:
            self.is_drag = True
            # マウスカーソル位置(X,Y)とウィンドウの起点(X,Y)の差を記録する
            self.drag_start_mouse_x = pyxel.mouse_x - self.get_abs_x()
            self.drag_start_mouse_y = pyxel.mouse_y - self.get_abs_y()
        else:
            super().on_mouse_down(btn, x, y)
    
    def on_mouse_up(self, btn, x, y):
        '''
        マウスボタンアップイベントハンドラ
        '''
        # ドラッグモード解除判定
        if self.is_drag == True:
            self.is_drag = False
        else:
            super().on_mouse_up(btn, x, y)
        
    def update_widget(self):
        if self.is_drag:
            self.x = pyxel.mouse_x - self.drag_start_mouse_x
            self.y = pyxel.mouse_y - self.drag_start_mouse_y
    
    def draw_widget(self):
        if self.focus:
            pyxel.rect(self.get_abs_x(), self.get_abs_y(), self.w, self.h, pyxel.COLOR_DARK_BLUE)
            pyxel.rect(self.get_abs_x() + 1, self.get_abs_y() + 1, self.w - 2, self.h - 2, pyxel.COLOR_LIGHT_BLUE)
        else:
            pyxel.rect(self.get_abs_x(), self.get_abs_y(), self.w, self.h, pyxel.COLOR_DARK_BLUE)
            pyxel.rect(self.get_abs_x() + 1, self.get_abs_y() + 1, self.w - 2, self.h - 2, pyxel.COLOR_WHITE)
        pyxel.rect(self.get_abs_x() + 2, self.get_abs_y() + 2, self.w - 4, self.h - 4, pyxel.COLOR_WHITE)
        
        if len(self.text) > 0: # タイトルバー有無判定
            pyxel.text(self.get_abs_x() + 2, self.get_abs_y() + 2, f'[ {self.text} ]', pyxel.COLOR_BLACK, _font)

class Image(Widget):
    '''
    イメージ
    '''
    def __init__(self, x=0, y=0, w=10, h=10):
        super().__init__(x, y, w, h)
        
    def update_widget(self):
        pass
    
    def draw_widget(self):
        pass

class Button(Widget):
    '''
    ボタン
    '''
    def __init__(self, text, x=0, y=0, w=10, h=10, color=0):
        super().__init__(x, y, w, h)
        self.text = text
        self.is_mouse_down = False
    
    def on_unfocus(self):
        '''
        フォーカス解除イベントハンドラ
        '''
        super().on_unfocus()
        self.is_mouse_down = False
    
    def on_mouse_down(self, btn, x, y):
        '''
        マウスボタンダウンイベントハンドラ
        '''
        super().on_mouse_down(btn, x, y)
        self.is_mouse_down = True
    
    def on_mouse_up(self, btn, x, y):
        '''
        マウスボタンアップイベントハンドラ
        '''
        super().on_mouse_up(btn, x, y)
        self.is_mouse_down = False
        
    def update_widget(self):
        # サイズの自動調整 (ざっくり)
        #self.w = len(self.text) * _FONT_WIDTH + 5
        self.w = 5
        for t in self.text:
            self.w += _FONT_WIDTH_ASCII if t.isascii() else _FONT_WIDTH_2BYTE
        self.h = _BUTTON_HEIGHT
        
        # ボタン範囲外移動判定
        if self.get_abs_x() <= pyxel.mouse_x and self.get_abs_y() <= pyxel.mouse_y and self.get_abs_x() + self.w >= pyxel.mouse_x and self.get_abs_y() + self.h >= pyxel.mouse_y:
            pass
        else:
            self.is_mouse_down = False
    
    def draw_widget(self):
        if self.is_mouse_down:
            pyxel.rect(self.get_abs_x(), self.get_abs_y(), self.w, self.h, pyxel.COLOR_DARK_BLUE)
            pyxel.rect(self.get_abs_x() + 1, self.get_abs_y() + 1, self.w - 2, self.h - 2, pyxel.COLOR_NAVY)
            pyxel.rect(self.get_abs_x() + 2, self.get_abs_y() + 2, self.w - 4, self.h - 4, pyxel.COLOR_BLACK)
            pyxel.text(self.get_abs_x() + 3, self.get_abs_y() + 3, self.text, pyxel.COLOR_WHITE, _font)
        else:
            pyxel.rect(self.get_abs_x(), self.get_abs_y(), self.w, self.h, pyxel.COLOR_DARK_BLUE)
            pyxel.rect(self.get_abs_x() + 1, self.get_abs_y() + 1, self.w - 2, self.h - 2, pyxel.COLOR_LIGHT_BLUE)
            pyxel.rect(self.get_abs_x() + 2, self.get_abs_y() + 2, self.w - 4, self.h - 4, pyxel.COLOR_WHITE)
            pyxel.text(self.get_abs_x() + 3, self.get_abs_y() + 3, self.text, pyxel.COLOR_BLACK, _font)

class Text(Widget):
    '''
    テキスト
    '''
    def __init__(self, text, x=0, y=0, w=10, h=10, color=0):
        super().__init__(x, y, w, h)
        self.text = text
        self.color = color
        
    def update_widget(self):
        # サイズの自動調整 (ざっくり)
        #self.w = len(self.text) * _FONT_WIDTH + 5
        self.w = 5
        for t in self.text:
            self.w += _FONT_WIDTH_ASCII if t.isascii() else _FONT_WIDTH_2BYTE
        self.h = _TEXT_HEIGHT
    
    def draw_widget(self):
        pyxel.text(self.get_abs_x(), self.get_abs_y(), self.text, self.color, _font)

# テストコード
if __name__ == '__main__':
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

    button = Button('ボタンA', 10, 30)
    def on_mouse_click_button(self, btn):
        global count
        count += 1
        text.text = f'カウントを集計 {count}'
        text.color = pyxel.COLOR_RED
    button.on_click = on_mouse_click_button.__get__(button, Button)
    window.append(widget=button)

    window2 = Window('', 20, 100, 100, 100)
    def update_window2(self):
        self.x += 0.1
    window2.on_update = update_window2.__get__(window2, Window)
    gui.append(widget=window2)

    image1 = Image(10, 30, 50, 50)
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

    print('Start Python GUI test')
    pyxel.run(update=update, draw=draw)
