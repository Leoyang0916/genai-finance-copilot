import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(page_title="GenAI Personal Finance Copilot", layout="wide")

st.title("GenAI Personal Finance Copilot")
st.subheader("個人化財務助手 Prototype")

# 讀取資料
@st.cache_data
def load_data():
    df = pd.read_csv("transactions.csv")
    return df

df = load_data()

# ===== 摘要區 =====
st.markdown("## 消費摘要")

total_spending = df["amount"].sum()
avg_spending = df["amount"].mean()

category_summary = df.groupby("category")["amount"].sum().sort_values(ascending=False)
top_category = category_summary.idxmax()

col1, col2, col3 = st.columns(3)
col1.metric("本月總支出", f"${total_spending:.2f}")
col2.metric("平均支出", f"${avg_spending:.2f}")
col3.metric("最大支出類別", top_category)

# ===== 表格與圖表 =====
st.markdown("## 類別支出分析")

st.dataframe(category_summary)
st.bar_chart(category_summary)

# ===== AI 問答 =====
st.markdown("## AI 財務問答")

api_key = st.text_input("請輸入 OpenAI API Key（可留空，使用 Demo 模式）", type="password")
user_question = st.text_input("請輸入你的問題")

if st.button("產生 AI 回答"):
    if not user_question:
        st.warning("請先輸入問題")
    else:
        try:
            if api_key:
                client = OpenAI(api_key=api_key)

                prompt = f"""
你是一位專業的銀行個人財務助手，請根據以下使用者消費資料回答問題。

【使用者消費資料】
{df.to_string()}

【使用者問題】
{user_question}

請用繁體中文回答，並遵守以下格式：
1. 消費概況（2-3句）
2. 重點觀察（條列 2-3 點）
3. 建議（條列 2-3 點）

請保持專業、清楚、簡潔，不要提供高風險投資建議。
"""

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )

                st.markdown("### AI 回答")
                st.write(response.choices[0].message.content)

            else:
                raise Exception("No API key provided")

        except Exception:
            top_amount = category_summary.iloc[0]

            # 根據問題簡單分類
            if "最多" in user_question or "哪裡" in user_question:
                advice = f"""
### AI 回答（Demo 模式）

**消費概況**  
你本月總支出為 **${total_spending:.2f}**，其中支出最高的類別是 **{top_category}**，金額為 **${top_amount:.2f}**。

**重點觀察**  
- 你的主要支出集中在 **{top_category}** 類別。  
- 此類別支出佔比相對較高，建議優先關注。  

**建議**  
- 檢視 {top_category} 類別中的消費是否有可減少的項目。  
- 若為日常支出，可考慮設定預算限制。
"""

            elif "減少" in user_question or "省" in user_question:
                advice = f"""
### AI 回答（Demo 模式）

**消費概況**  
你本月總支出為 **${total_spending:.2f}**，其中 **{top_category}** 是最大支出來源。

**重點觀察**  
- {top_category} 類別支出較高，是主要節省空間。  
- 部分支出可能屬於可調整項目。  

**建議**  
- 優先降低 {top_category} 類別的支出比例。  
- 建議設定每週或每月預算上限。  
- 可透過記帳或提醒機制控制消費頻率。
"""

            else:
                advice = f"""
### AI 回答（Demo 模式）

**消費概況**  
你的總支出為 **${total_spending:.2f}**，主要集中在 **{top_category}**。

**重點觀察**  
- 支出集中度較高。  
- 部分類別可能存在優化空間。  

**建議**  
- 建立預算規劃  
- 定期檢視消費習慣  
"""

            st.markdown(advice)
            st.info("目前為 Demo 模式，正式版本可串接 LLM 提供更精準回答。")