# app.py

import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster, HeatMap
import pandas as pd

# 타이틀ls
st.title("📹 진주시 CCTV 설치 현황 분석")

# CSV 불러오기
df = pd.read_csv("경상남도 진주시_CCTV위치정보_20250501.csv", encoding="euc-kr")

# 위도/경도 컬럼 명 변경
df = df.rename(columns={"위도": "lat", "경도": "lon", "목적": "purpose", "설치장소": "location"})

# 데이터 출력
st.subheader("📄 원본 데이터")
st.dataframe(df, height=250)

# 기본 지도 설정
m = folium.Map(location=[35.1799817, 128.1076213], zoom_start=13)

# 마커 클러스터 추가
st.subheader("📍 CCTV 위치 (MarkerCluster)")
marker_cluster = MarkerCluster().add_to(m)
for _, row in df.iterrows():
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=f"<b>장소:</b> {row['location']}<br><b>목적:</b> {row['purpose']}",
    ).add_to(marker_cluster)

# 히트맵 체크박스
if st.checkbox("🔥 히트맵 보기 (설치 밀집도)"):
    HeatMap(df[["lat", "lon"]]).add_to(m)

# folium 지도 렌더링
folium_static(m)

# 목적별 CCTV 설치 통계
st.subheader("📊 CCTV 목적별 설치 통계")
purpose_counts = df["purpose"].value_counts()
st.bar_chart(purpose_counts)
