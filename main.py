from linebot.models import TextSendMessage
import openai
import json

with open('key.json','r') as f:
    key = json.load(f)

openai.api_key = key["openai_key"]


class OpenAI_service():
    def __init__(self,message,user):
        self.message = message
        self.user_name = user
    def get_response(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 或其他你有權限使用的模型
            messages=[
                {"role": "system", "content": 
                 
"""你是一個樂於助人的工程助理，專門協助工程師解決技術問題和優化設計方案。你的職責包括深入理解工程問題，經過深思熟慮後提供清晰、專業且可行的解決方案。你的回答應該邏輯嚴謹，並根據實際應用場景提供合理的分析與建議。  

### 指導原則：  
1. **專業與準確性**：基於工程原理和最佳實踐，確保建議具有可行性和實用價值。  
2. **清晰與條理**：用簡潔且有結構的方式回答問題，使工程師能夠迅速理解並應用。  
3. **深思熟慮**：在回答之前，充分考慮問題的背景、可能的挑戰及多種解決方案，並比較其優劣。  
4. **積極協助**：主動提供附加建議，如優化方法、潛在風險以及改進的可能性。  
5. **實踐導向**：結合實際工程應用，舉例說明解決方案如何實施，並提供相應的技術資源或工具建議。  

### 回應格式：  
- **問題分析**：闡述問題的本質與關鍵因素。  
- **可能解決方案**：列舉多種可行方案並比較其優缺點。  
- **最佳建議**：根據情境選擇最適合的方案並詳細說明實施步驟。  
- **潛在風險與優化建議**：提出可能遇到的困難及其對策，確保方案可行性。  

你的目標是以專業、高效且富有條理的方式協助工程師，使其能夠快速找到最佳解決方案並提高工作效率。"""

                },#用來設定助手的角色或行為指導
                {"role": "user", "content": self.message}#表示用戶的提問
            ]
        )
        return response.choices[0].message["content"]



class user_data():
    def __init__(self,name:str,message:str):
        self.user_name = name
        self.message = message
def reply_message(event):
    #輸入的訊息
    message = TextSendMessage(text=event.message.text)
    #用戶的名稱
    user = event.source.user_id

    reply_message = OpenAI_service.get_response(message,user)
    return reply_message
