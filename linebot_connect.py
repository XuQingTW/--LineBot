import json

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from main import reply_message

# 讀取金鑰設定檔
with open('key.json', 'r') as f:
    key = json.load(f)

app = Flask(__name__)

# 設定 Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi(key["line_Channel_access_token"])
handler = WebhookHandler(key["line_Channel_secret"])


@app.route("/callback", methods=['POST'])
def callback():
    """處理來自 LINE 平台的 callback 請求."""
    # 以安全方式取得 X-Line-Signature 標頭
    signature = request.headers.get('X-Line-Signature')
    # 取得請求的 body
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    """處理收到的文字訊息事件."""
    # 呼叫 reply_message 取得要回覆的訊息內容
    message = reply_message(event)
    # 使用 event.reply_token 來回覆訊息
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    app.run(port=8000)
