pyxel = None

class Widget:
    '''
    ウィジェットのベースクラス
    '''
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 32
        self.h = 32
        self.enable = True
        self.visible = True
        self.own = None
        self.widgets = []
        self.on_update = None
        self.on_draw = None
        self.on_click = None
        
    def append(self, widget):
        self.widgets.append(widget)
        widget.own = self
    
    def remove(self, widget):
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
            if self.on_update != None:
                self.on_update(sender=self)
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
            self.draw_widget()
            if self.on_draw != None:
                self.on_draw(sender=self)
            for widget in self.widgets:
                widget.draw()

class PyxelGui(Widget):
    '''
    画面構成上のトップレイヤー
    イベント配送処理は本関数内に実装する
    '''
    def __init__(self, pyxel_ref):
        super().__init__()
        global pyxel
        pyxel = pyxel_ref
        
    def update_widget(self):
        pass
    
    def draw_widget(self):
        pyxel.cls(pyxel.COLOR_BLACK)

class Window(Widget):
    '''
    ウィンドウ
    '''
    def __init__(self):
        super().__init__()
        
    def update_widget(self):
        pass
    
    def draw_widget(self):
        pyxel.rect(self.own.x + self.x, self.own.y + self.y, self.w, self.h, pyxel.COLOR_WHITE)

class Image(Widget):
    '''
    イメージ
    '''
    def __init__(self):
        super().__init__()
        
    def update_widget(self):
        pass
    
    def draw_widget(self):
        pass

class Button(Widget):
    '''
    ボタン
    '''
    def __init__(self, text):
        super().__init__()
        self.text = text
        
    def update_widget(self):
        pass
    
    def draw_widget(self):
        # ボタンサイズの自動調整
        self.w = len(self.text) * 4 + 4
        self.h = 9
        
        pyxel.rectb(self.own.x + self.x, self.own.y + self.y, self.w, self.h, pyxel.COLOR_BLACK)
        pyxel.text(self.own.x + self.x + 2, self.own.y + self.y + 2, self.text, pyxel.COLOR_BLACK)

class Text(Widget):
    '''
    テキスト
    '''
    def __init__(self, text):
        super().__init__()
        self.text = text
        
    def update_widget(self):
        pass
    
    def draw_widget(self):
        pyxel.text(self.own.x + self.x, self.own.y + self.y, self.text, pyxel.COLOR_BLACK)
