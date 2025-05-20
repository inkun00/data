import streamlit as st
import folium
from folium import plugins
from io import BytesIO
import base64

# 앱 타이틀
st.title("생태지도 앱")

# 지도 초기화 (위도, 경도, 줌 레벨 설정)
m = folium.Map(location=[37.5665, 126.978], zoom_start=12)

# Streamlit 입력란: 메모 입력
memo = st.text_area("해당 위치에 대한 메모를 작성하세요:")

# Folium 마커 클릭 시 메모 추가하는 함수
def add_marker_on_click(event):
    lat, lon = event.latlng
    folium.Marker([lat, lon], popup=memo).add_to(m)
    st.write(f"북마크가 추가된 위치: 위도: {lat}, 경도: {lon}")

# Folium 지도에서 클릭을 처리하기 위한 LatLngPopup
popup = folium.LatLngPopup()
m.add_child(popup)

# 지도 표시
def map_to_html(m):
    map_html = m._repr_html_()
    return map_html

# 지도 HTML로 변환 후 Streamlit에서 표시
st.markdown(map_to_html(m), unsafe_allow_html=True)
