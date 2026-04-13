# GenAI Personal Finance Copilot

## 專案簡介
本專案是一個以 GenAI 為核心的個人化財務助手 Prototype，模擬銀行場景中的客戶財務管理應用。

系統可根據使用者交易資料，自動產生消費摘要、類別分析，並透過自然語言問答提供個人化財務建議。

## 主要功能
- 每月消費摘要
- 類別支出分析
- 自然語言財務問答
- 個人化財務建議（Demo 模式）

## 技術架構
- Python
- Streamlit
- Pandas
- OpenAI API（選用）
- Demo fallback mode

## 使用方式
1. 開啟 Streamlit app
2. 查看消費摘要與支出分析
3. 輸入問題，例如：
   - 我這個月花最多在哪？
   - 我可以怎麼減少支出？
4. 系統會根據資料提供財務觀察與建議

## 檔案說明
- `app.py`：主程式
- `transactions.csv`：模擬交易資料
- `requirements.txt`：套件需求清單

## 備註
目前 Prototype 為了快速驗證使用情境，提供 Demo 模式回答。  
若正式上線，可串接 LLM API，提供更即時且更完整的個人化生成能力。

## 專案目的
此專案用於展示 GenAI 如何應用於銀行客戶場景，將原始交易數據轉化為更容易理解的財務洞察與決策建議。
