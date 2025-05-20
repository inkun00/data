import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("글로벌 시가총액 TOP10 기업의 최근 1년간 주가 변화 (Plotly)")

# 글로벌 시가총액 TOP10 (2024년 기준, 필요시 업데이트 가능)
top10_tickers = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Nvidia": "NVDA",
    "Saudi Aramco": "2222.SR",
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "Meta (Facebook)": "META",
    "Berkshire Hathaway": "BRK-B",
    "Eli Lilly": "LLY",
    "TSMC": "TSM"
}

st.markdown("#### 최근 1년간 글로벌 시가총액 Top10 기업의 종가 비교")

# 날짜 계산
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# 데이터 다운로드
@st.cache_data(show_spinner=True)
def load_data(tickers, start, end):
    data = {}
    for name, ticker in tickers.items():
        df = yf.download(ticker, start=start, end=end)
        if not df.empty:
            data[name] = df["Close"]
    return pd.DataFrame(data)

with st.spinner("야후 파이낸스에서 데이터 가져오는 중..."):
    df_close = load_data(top10_tickers, start_date, end_date)

# 결측치 보정(보수적)
df_close.fillna(method='ffill', inplace=True)
df_close.fillna(method='bfill', inplace=True)

# Plotly 그래프
fig = go.Figure()
for name in df_close.columns:
    fig.add_trace(go.Scatter(x=df_close.index, y=df_close[name], mode='lines', name=name))
fig.update_layout(title="글로벌 시가총액 Top10 기업의 최근 1년간 주가 변화",
                  xaxis_title="날짜", yaxis_title="종가(현지통화)", template="plotly_white",
                  legend_title="기업명")
st.plotly_chart(fig, use_container_width=True)

st.caption("데이터 출처: 야후 파이낸스 | *화폐 단위는 각 기업의 현지 통화 기준입니다.*")
