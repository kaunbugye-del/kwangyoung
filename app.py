import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"

import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(page_title="광영고 주변 음식점 지도", layout="wide")

# -------------------------------
# 🔧 사이드바 설정
# -------------------------------
st.sidebar.title("⚙️ 지도 설정")

# ✅ 테마 선택 제거 → 항상 기본 지도(OpenStreetMap)
tile_style = "OpenStreetMap"

# 음식 종류 필터
category = st.sidebar.selectbox("🍴 음식 종류 선택", ["전체", "식사", "간식", "기타"])

# 줌 설정
zoom_level = st.sidebar.slider("🔍 지도 확대/축소", 15, 18, 15)

# 검색 기능
search_query = st.sidebar.text_input("🔍 음식점 이름 검색", placeholder="예: 쥬씨")

# -------------------------------
# 📍 음식점 데이터
# -------------------------------
places = [
    {"name": "금화왕 돈까스", "info": "돈까스 소스 16, 샐러드 12.5, 딸기잼 30", 
     "lat": 37.53976476914723, "lon": 126.83216235565537, "category": "기타"},
    {"name": "쥬씨", "info": "블루베리 8, 토마토 8, 초코바나나 20, 수박 11", 
     "lat": 37.53876476914723, "lon": 126.82816235565537, "category": "간식"},
    {"name": "명랑핫도그", "info": "치즈핫도그 15, 감자핫도그 10, 오징어 7", 
     "lat": 37.53776476914723, "lon": 126.82616235565537, "category": "간식"},
    {"name": "전주가", "info": "제육볶음 소스 21", 
     "lat": 37.5264285, "lon": 126.8342266, "category": "기타"},
    {"name": "수수팥", "info": "꿀떡 3.2", 
     "lat": 37.5411795385261, "lon": 126.833513722931, "category": "간식"},
    {"name": "철이네분식", "info": "떡꼬치 소스 13", 
     "lat": 37.5378272, "lon": 126.8281213, "category": "기타"},
    {"name": "오도르베이커리", "info": "생크림 24", 
     "lat": 37.541147, "lon": 126.8376476, "category": "기타"},
    {"name": "메가커피", "info": "딸기라떼 7 , 아이스초코 17", 
     "lat": 37.5395476, "lon": 126.8336208, "category": "간식"},
    {"name": "뚜레쥬르", "info": "식빵 14", 
     "lat": 37.5294857, "lon": 126.8330209, "category": "간식"},
    {"name": "파리바게뜨", "info": "꽈배기 9", 
     "lat": 37.522121, "lon": 126.8333182, "category": "간식"},
    {"name": "복호두", "info": "호두과자 9", 
     "lat": 37.5444411, "lon": 126.8388041, "category": "간식"},
    {"name": "커피에반하다", "info": "초코라떼 16", 
     "lat": 37.5328904, "lon": 126.8371200, "category": "간식"},  # ← 위도 오류 수정
    {"name": "컴포즈커피", "info": "초코 19", 
     "lat": 37.5410422, "lon": 126.838965, "category": "기타"},
    {"name": "맘스터치", "info": "싸이버거 30", 
     "lat": 37.5411987, "lon": 126.8377784, "category": "식사"},
    {"name": "토마토김밥", "info": "토마토김밥 20", 
     "lat": 37.5335091, "lon": 126.837202, "category": "식사"},
    {"name": "맥도날드", "info": "불고기버거 30", 
     "lat": 37.5314392, "lon": 126.8309681, "category": "식사"},
    {"name": "버거킹", "info": "와퍼 30", 
     "lat": 37.5391241, "lon": 126.8292262, "category": "식사"}    
]

# -------------------------------
# 🎨 지도 생성
# -------------------------------
center_lat, center_lon = 37.53758714716197, 126.82327111433354

searched_place = None
for place in places:
    if search_query and search_query.strip() in place["name"]:
        searched_place = place
        break

if searched_place:
    map_center = [searched_place["lat"], searched_place["lon"]]
    zoom_level = 17
else:
    map_center = [center_lat, center_lon]

# ✅ 기본 지도만 사용
m = folium.Map(location=map_center, zoom_start=zoom_level, tiles=tile_style)

# -------------------------------
# 📍 마커 표시
# -------------------------------
for place in places:
    if category != "전체" and place["category"] != category:
        continue

    popup_html = f"""
    <div style="font-family:sans-serif; text-align:left; padding:5px; width:220px;">
        <h4 style="margin-bottom:5px; color:#333;">{place['name']}</h4>
        <p style="font-size:13px; margin:0; color:#555;">🍽️ {place['category']}</p>
        <p style="font-size:12px; margin:4px 0;">{place['info']}</p>
    </div>
    """

    marker = folium.Marker(
        location=[place["lat"], place["lon"]],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=place["name"],
        icon=folium.Icon(color="blue", icon="cutlery")
    )
    marker.add_to(m)

# -------------------------------
# 🗺️ 지도 출력
# -------------------------------
st.markdown(
    """
    <h1 style='text-align:center; font-size:38px; font-weight:600; margin-bottom:15px;'>
        📍 광영고 주변 음식점 지도
    </h1>
    """, unsafe_allow_html=True
)

st_folium(m, width=1000, height=600, returned_objects=[])