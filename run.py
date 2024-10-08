from flask import Flask, Request, Response
import webbrowser

app = Flask(__name__, static_folder='.', static_url_path='/')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# ゲーム画面用HTML
html = '''
<html>
    <head>
        <meta charset="utf-8">
        <title>Game</title>
    </head>
    <body>
        <script src="https://cdn.jsdelivr.net/gh/kitao/pyxel/wasm/pyxel.js"></script>
        {}
    </body>
</html>
'''

tag_app = '''
<pyxel-run root="." name="pyxelgui.py" gamepad="disabled" packages=""></pyxel-run>
'''
tag_edit = '''
<pyxel-edit root="." name="resources.pyxres" editor="image"></pyxel-edit>'''

html_app = html.format(tag_app)
html_edit = html.format(tag_edit)


# リソースファイルを取得するGETハンドラ
@app.route('/', methods=['GET'])
def get_app():
    return html_app
    
@app.route('/edit', methods=['GET'])
def get_edit():
    return html_edit

# エントリポイント
if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5000
    url_app = 'http://{}:{}/'.format(host, port)
    url_edit = 'http://{}:{}/edit'.format(host, port)
    print('app  : {}'.format(url_app))
    print('edit : {}'.format(url_edit))
    print('please open in safari secret mode.'.format(url_edit))

    webbrowser.open(url_app)

    app.run(host=host, port=port)

