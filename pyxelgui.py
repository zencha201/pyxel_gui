pyxel = None

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
        self.own = None
        self.widgets = []
    
    def on_focus(self):
        '''
        フォーカスイベントハンドラ
        '''
        pass
    
    def on_unfocus(self):
        '''
        フォーカス解除イベントハンドラ
        '''
        pass
    
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
            ox = self.own.x if self.own != None else 0
            oy = self.own.y if self.own != None else 0
            pyxel.clip(ox + self.x, oy + self.y, self.w, self.h)
            
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
    def __init__(self, pyxel_ref):
        global pyxel
        pyxel = pyxel_ref
        super().__init__(0, 0, pyxel.width, pyxel.height)
        pyxel.mouse(True)
        
        # マウスイベント関係
        self.mouse_x = pyxel.mouse_x
        self.mouse_y = pyxel.mouse_y
        self.mouse_btn = {pyxel.MOUSE_BUTTON_LEFT : False, 
                          pyxel.MOUSE_BUTTON_MIDDLE : False, 
                          pyxel.MOUSE_BUTTON_RIGHT : False}
    
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
        pyxel.cls(pyxel.COLOR_BLACK)

class Window(Widget):
    '''
    ウィンドウ
    '''
    def __init__(self, text, x=0, y=0, w=100, h=80, color=0):
        super().__init__(x, y, w, h)
        self.text = text
        
    def update_widget(self):
        pass
    
    def draw_widget(self):
        pyxel.rect(self.own.x + self.x, self.own.y + self.y, self.w, self.h, pyxel.COLOR_WHITE)
        pyxel.text(self.own.x + self.x + 2, self.own.y + self.y + 2, f'[ {self.text} ]', pyxel.COLOR_BLACK)

class Image(Widget):
    '''
    イメージ
    '''
    def __init__(self):
        super().__init__(0, 0, 0, 0)
        
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
        self.w = len(self.text) * 4 + 4
        self.h = 9
    
    def draw_widget(self):
        if self.is_mouse_down:
            pyxel.rect(self.own.x + self.x, self.own.y + self.y, self.w, self.h, pyxel.COLOR_NAVY)
            pyxel.rectb(self.own.x + self.x, self.own.y + self.y, self.w, self.h, pyxel.COLOR_BLACK)
            pyxel.text(self.own.x + self.x + 2, self.own.y + self.y + 2, self.text, pyxel.COLOR_WHITE)
        else:
            pyxel.rect(self.own.x + self.x, self.own.y + self.y, self.w, self.h, pyxel.COLOR_WHITE)
            pyxel.rectb(self.own.x + self.x, self.own.y + self.y, self.w, self.h, pyxel.COLOR_BLACK)
            pyxel.text(self.own.x + self.x + 2, self.own.y + self.y + 2, self.text, pyxel.COLOR_BLACK)

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
        self.w = len(self.text) * 4 + 4
        self.h = 9
    
    def draw_widget(self):
        pyxel.text(self.own.x + self.x, self.own.y + self.y, self.text, self.color)
