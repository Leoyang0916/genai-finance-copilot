import streamlit as st
import pandas as pd

st.set_page_config(page_title="GenAI Personal Finance Copilot", layout="wide")

st.title("GenAI Personal Finance Copilot")
st.subheader("個人化財務助手 Prototype")

# ===== 直接內建資料，避免 CSV 問題 =====
data = [
    {"date": "2026-04-01", "category": "Food", "merchant": "McDonald's", "amount": 18.5},
    {"date": "2026-04-02", "category": "Transport", "merchant": "Opal", "amount": 6.2},
    {"date": "2026-04-03", "category": "Shopping", "merchant": "Uniqlo", "amount": 89.0},
    {"date": "2026-04-04", "category": "Food", "merchant": "Woolworths", "amount": 45.7},
    {"date": "2026-04-05", "category": "Entertainment", "merchant": "Netflix", "amount": 17.99},
    {"date": "2026-04-06", "category": "Food", "merchant": "Starbucks", "amount": 8.5},
    {"date": "2026-04-07", "category": "Transport", "merchant": "Uber", "amount": 22.4},
    {"date": "2026-04-08", "category": "Shopping", "merchant": "Kmart", "amount": 35.6},
    {"date": "2026-04-09", "category": "Bills", "merchant": "Electricity", "amount": 75.0},
    {"date": "2026-04-10", "category": "Food", "merchant": "Coles", "amount": 52.3},
    {"date": "2026-04-11", "category": "Entertainment", "merchant": "Spotify", "amount": 11.99},
    {"date": "2026-04-12", "category": "Shopping", "merchant": "Amazon", "amount": 120.0},
    {"date": "2026-04-13", "category": "Transport", "merchant": "Opal", "amount": 5.8},
    {"date": "2026-04-14", "category": "Food", "merchant": "Subway", "amount": 12.5},
    {"date": "2026-04-15", "category": "Bills", "merchant": "Internet", "amount": 65.0},
]

df = pd.DataFrame(data)

# ===== 摘要區 =====
st.markdown("## 消費摘要")

total_spending = df["amount"].sum()
avg_spending = df["amount"].mean()

category_summary = (
    df.groupby("category", as_index=False)["amount"]
    .sum()
    .sort_values(by="amount", ascending=False)
)

top_category = category_summary.iloc[0]["category"]
top_amount = category_summary.iloc[0]["amount"]

col1, col2, col3 = st.columns(3)
col1.metric("本月總支出", f"${total_spending:.2f}")
col2.metric("平均單筆支出", f"${avg_spending:.2f}")
col3.metric("最大支出類別", f"{top_category} (${top_amount:.2f})")

# ===== 類別分析 =====
st.markdown("## 類別支出分析")

left, right = st.columns(2)

with left:
    st.dataframe(category_summary, use_container_width=True)

with right:
    chart_df = category_summary.set_index("category")
    st.bar_chart(chart_df)

# ===== 原始資料 =====
with st.expander("查看原始交易資料"):
    st.dataframe(df, use_container_width=True)

# ===== Demo 問答 =====
st.markdown("## AI 財務問答（Demo 模式）")

preset = st.selectbox(
    "請選擇問題",
    [
        "",
        "我這個月花最多在哪？",
        "我可以怎麼減少支出？",
        "我的消費習慣有什麼需要注意的地方？",
    ],
)

custom_q = st.text_input("或自行輸入問題")
user_question = custom_q if custom_q else preset

if st.button("產生 AI 回答"):
    if not user_question:
        st.warning("請先輸入或選擇問題")
    else:
        if "最多" in user_question or "哪裡" in user_question:
            answer = f"""
### AI 回答（Demo 模式）

**消費概況**  
你本月總支出為 **${total_spending:.2f}**，目前支出最高的類別是 **{top_category}**，金額為 **${top_amount:.2f}**。

**重點觀察**  
- 你的主要支出集中在 **{top_category}** 類別。  
- 此類別目前是最值得優先關注的支出來源。  

**建議**  
- 先檢視 **{top_category}** 中是否有可調整或可替代的花費。  
- 若屬於日常消費，建議設定每月預算上限。
"""
        elif "減少" in user_question or "省" in user_question:
            answer = f"""
### AI 回答（Demo 模式）

**消費概況**  
你本月總支出為 **${total_spending:.2f}**，其中 **{top_category}** 是最大支出來源。

**重點觀察**  
- **{top_category}** 類別支出較高，是最有節省空間的部分。  
- 如果沒有預算控制，這類支出容易持續累積。  

**建議**  
- 優先降低 **{top_category}** 類別的支出比例。  
- 建議設定每週或每月預算上限。  
- 可以透過記帳或消費提醒，降低非必要支出頻率。
"""
        else:
            answer = f"""
### AI 回答（Demo 模式）

**消費概況**  
你的本月總支出為 **${total_spending:.2f}**，支出主要集中在 **{top_category}** 類別。

**重點觀察**  
- 目前支出集中度偏高。  
- 若缺乏預算管理，可能影響儲蓄空間。  

**建議**  
- 建立每月預算規劃。  
- 定期檢視消費類別分布。  
- 優先追蹤高支出項目的變化。
"""
        st.markdown(answer)
        st.info("此版本為 Demo 模式，用於展示 GenAI 財務助手的互動流程與商業概念。")