from linebot.models import TextSendMessage

class user_data():
    def __init__(self,name:str,message:str):
        self.user_name = name
        self.message = message
def reply_message(event):
    #輸入的訊息
    message = TextSendMessage(text=event.message.text)
    #用戶的名稱
    user = event.source.user_id
