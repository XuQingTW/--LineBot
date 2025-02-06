from linebot import LineBotApi
from linebot.models import TextSendMessage

# 假設已經在其他地方設定好 Channel Access Token
LINE_CHANNEL_ACCESS_TOKEN = "你的 Channel Access Token"
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

class user_data:
    def __init__(self, name: str, message: str):
        self.user_name = name
        self.message = message

def reply_message(event):
    # 取得使用者傳入的訊息文字
    user_msg = event.message.text
    # 取得使用者的ID（或其他識別資訊）
    user_id = event.source.user_id

    # 將資訊封裝到user_data物件中（視需要進行後續處理）
    data = user_data(name=user_id, message=user_msg)

    # 準備回覆訊息，這邊直接回傳收到的訊息內容
    response = TextSendMessage(text=f"你傳送的訊息是: {data.message}")

    # 使用line_bot_api將回覆訊息發送回使用者
    line_bot_api.reply_message(event.reply_token, response)

