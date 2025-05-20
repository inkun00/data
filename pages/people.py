
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import re

st.set_page_config(layout="wide")
st.title("서울시 인구 통계 시각화 (남녀구분, 남여합계)")

# 파일 업로드
남녀구분_file = st.file_uploader("남녀구분.csv 파일을 업로드하세요", type="csv")
남여합계_file = st.file_uploader("남여합계.csv 파일을 업로드하세요", type="csv")

if 남녀구분_file and 남여합계_file:
    # 데이터 불러오기
    df1 = pd.read_csv(남녀구분_file, encoding="cp949")
    df2 = pd.read_csv(남여합계_file, encoding="cp949")

    ### 1. 서울특별시 전체 연령별 남녀 분포
    df1_seoul = df1[df1['행정구역'].str.contains('서울특별시 ') & ~df1['행정구역'].str.contains('구')].iloc[0]
    male_cols = [col for col in df1.columns if re.match(r'2025년04월_남_\d+세|2025년04월_남_100세 이상', col)]
    female_cols = [col for col in df1.columns if re.match(r'2025년04월_여_\d+세|2025년04월_여_100세 이상', col)]
    ages = [re.findall(r'(\d+세|100세 이상)', col)[0] for col in male_cols]
    male_pop = df1_seoul[male_cols].str.replace(',', '').fillna(0).astype(int)
    female_pop = df1_seoul[female_cols].str.replace(',', '').fillna(0).astype(int)

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=ages, y=male_pop, mode='lines+markers', name='남자'))
    fig1.add_trace(go.Scatter(x=ages, y=female_pop, mode='lines+markers', name='여자'))
    fig1.update_layout(title='서울특별시 연령별 남녀 인구 분포',
                      xaxis_title='연령', yaxis_title='인구수', template='plotly_white')
    st.plotly_chart(fig1, use_container_width=True)

    ### 2. 행정구역별(구) 남녀 비율 비교
    df1_gu = df1[df1['행정구역'].str.contains('서울특별시 ') & df1['행정구역'].str.contains('구 ')]
    df1_gu['구'] = df1_gu['행정구역'].apply(lambda x: re.findall(r'서울특별시\s(.+?)\s', x)[0])
    df1_gu['남'] = df1_gu['2025년04월_남_총인구수'].str.replace(',', '').astype(int)
    df1_gu['여'] = df1_gu['2025년04월_여_총인구수'].str.replace(',', '').astype(int)
    fig2 = go.Figure(data=[
        go.Bar(name='남자', x=df1_gu['구'], y=df1_gu['남']),
        go.Bar(name='여자', x=df1_gu['구'], y=df1_gu['여'])
    ])
    fig2.update_layout(barmode='group', title='서울시 구별 남녀 인구수', xaxis_title='구', yaxis_title='인구수')
    st.plotly_chart(fig2, use_container_width=True)

    ### 3. 행정구역별(구) 전체 인구 분포
    df2_gu = df2[df2['행정구역'].str.contains('서울특별시 ') & df2['행정구역'].str.contains('구 ')]
    df2_gu['구'] = df2_gu['행정구역'].apply(lambda x: re.findall(r'서울특별시\s(.+?)\s', x)[0])
    df2_gu['합계'] = df2_gu['2025년04월_계_총인구수'].str.replace(',', '').astype(int)
    fig3 = go.Figure(data=[
        go.Bar(x=df2_gu['구'], y=df2_gu['합계'])
    ])
    fig3.update_layout(title='서울시 구별 전체 인구수', xaxis_title='구', yaxis_title='인구수')
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("두 개의 CSV 파일(남녀구분, 남여합계)을 모두 업로드해주세요.")
