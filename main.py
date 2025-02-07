from linebot.models import TextSendMessage
import openai
import json

# 載入 API 金鑰
with open('key.json', 'r') as f:
    keys = json.load(f)
openai.api_key = keys["openai_key"]

# 將系統提示訊息提取為常數，便於管理與維護
SYSTEM_PROMPT = """
你是一個樂於助人的工程助理，專門協助工程師解決技術問題和優化設計方案。你的職責包括深入理解工程問題，經過深思熟慮後提供清晰、專業且可行的解決方案。你的回答應該邏輯嚴謹，並根據實際應用場景提供合理的分析與建議。  

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

你的目標是以專業、高效且富有條理的方式協助工程師，使其能夠快速找到最佳解決方案並提高工作效率。
"""

class OpenAIService:
    """
    與 OpenAI ChatCompletion API 互動的服務類別。
    """
    def __init__(self, user_message: str, user_id: str) -> None:
        self.user_message = user_message
        self.user_id = user_id

    def get_response(self) -> str:
        """
        呼叫 OpenAI API 以取得回應訊息。

        Returns:
            str: 回應內容的文字。
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": self.user_message}
                ]
            )
            return response.choices[0].message["content"]
        except Exception as e:
            # 這裡可以進一步記錄 log 或進行錯誤處理
            return f"Error: {str(e)}"

class UserData:
    """
    儲存使用者資訊的資料類別，目前尚未使用，但可供未來擴展。
    """
    def __init__(self, name: str, message: str) -> None:
        self.user_name = name
        self.message = message

def reply_message(event) -> TextSendMessage:
    """
    處理傳入的 event，呼叫 OpenAI 取得回應，並返回 TextSendMessage 物件。

    Args:
        event: 包含使用者訊息與來源資訊的事件物件。

    Returns:
        TextSendMessage: 封裝回應文字的訊息物件。
    """
    # 直接提取文字訊息
    user_message_text = event.message.text
    user_id = event.source.user_id

    # 使用 OpenAIService 取得回應
    ai_service = OpenAIService(user_message_text, user_id)
    response_text = ai_service.get_response()

    return TextSendMessage(text=response_text)
