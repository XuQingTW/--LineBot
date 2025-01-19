from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

#登入https://developers.line.biz/zh-hant/

app = Flask(__name__)

# 設定 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = "你的 Channel Access Token"
LINE_CHANNEL_SECRET = "你的 Channel Secret"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # 獲取 X-Line-Signature 標頭
    signature = request.headers['X-Line-Signature']
    # 獲取請求的 body
    body = request.get_data(as_text=True)

    try:
        # 驗證請求並處理事件
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 處理文字訊息事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    reply_message = f"你說了: {event.message.text}"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

if __name__ == "__main__":
    app.run(port=8000)
