import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import math
from deep_translator import GoogleTranslator

KAKAO_API_KEY = "fc59295141197b8cf11c0c47dfa5c92c"

languages = {
    "한국어": "ko", "English": "en", "日本語": "ja", "中文(简体)": "zh-CN",
    "Español": "es", "Français": "fr", "Deutsch": "de", "Italiano": "it",
    "Português": "pt", "Русский": "ru", "العربية": "ar", "हिन्दी": "hi",
    "Bahasa Indonesia": "id", "Tiếng Việt": "vi", "ภาษาไทย": "th",
    "Türkçe": "tr", "Polski": "pl", "Nederlands": "nl", "Svenska": "sv",
    "Ελληνικά": "el", "Українська": "uk", "עברית": "he", "Swahili": "sw",
}

courses = [
    {"id": 1, "name": "서쪽 해안 드라이브", "difficulty": "쉬움", "duration": "2시간", "spots": ["협재해수욕장", "한림공원", "애월해안도로"], "recommended_vehicle": ["소형", "중형"]},
    {"id": 2, "name": "성산 일출 코스", "difficulty": "쉬움", "duration": "3시간", "spots": ["성산일출봉", "광치기해변", "섭지코지"], "recommended_vehicle": ["소형", "중형", "대형"]},
    {"id": 3, "name": "한라산 둘레길 코스", "difficulty": "보통", "duration": "4시간", "spots": ["1100고지", "어리목", "영실"], "recommended_vehicle": ["중형", "SUV"]},
    {"id": 4, "name": "남쪽 올레길 코스", "difficulty": "쉬움", "duration": "3시간", "spots": ["천지연폭포", "정방폭포", "외돌개"], "recommended_vehicle": ["소형", "중형"]},
    {"id": 5, "name": "동쪽 해녀 문화 코스", "difficulty": "쉬움", "duration": "3시간", "spots": ["김녕해수욕장", "월정리해변", "세화해변"], "recommended_vehicle": ["소형", "중형"]},
    {"id": 6, "name": "북쪽 감귤밭 코스", "difficulty": "보통", "duration": "3시간", "spots": ["다랑쉬오름", "비자림", "만장굴"], "recommended_vehicle": ["중형", "SUV"]},
    {"id": 7, "name": "제주시 야경 코스", "difficulty": "쉬움", "duration": "2시간", "spots": ["사라봉", "별도봉", "제주항"], "recommended_vehicle": ["소형", "중형"]},
    {"id": 8, "name": "서귀포 감성 카페 코스", "difficulty": "쉬움", "duration": "2시간", "spots": ["카멜리아힐", "서귀포매일올레시장", "이중섭거리"], "recommended_vehicle": ["소형", "중형"]},
    {"id": 9, "name": "우도 당일치기 코스", "difficulty": "쉬움", "duration": "4시간", "spots": ["우도봉", "홍조단괴해변", "검멀레해변"], "recommended_vehicle": ["소형"]},
    {"id": 10, "name": "중산간 힐링 코스", "difficulty": "보통", "duration": "3시간", "spots": ["산굼부리", "절물자연휴양림", "교래자연휴양림"], "recommended_vehicle": ["중형", "SUV"]},
]

school_zones = [
    {"name": "제주북초등학교 스쿨존", "lat": 33.5145, "lng": 126.5312},
    {"name": "신제주초등학교 스쿨존", "lat": 33.4892, "lng": 126.4789},
    {"name": "성산초등학교 스쿨존", "lat": 33.4507, "lng": 126.9196},
    {"name": "서귀포초등학교 스쿨존", "lat": 33.2530, "lng": 126.5600},
    {"name": "한림초등학교 스쿨존", "lat": 33.4139, "lng": 126.2661},
]

def translate(text, lang_code):
    if lang_code == "ko":
        return text
    try:
        return GoogleTranslator(source="ko", target=lang_code).translate(text)
    except:
        return text

def calculate_danger_score(place_name, category):
    score = 0
    if "기계식" in place_name or "기계식" in category:
        score += 40
    if "스쿨존" in place_name or "어린이" in place_name:
        score += 20
    if score >= 50:
        level = "🔴 위험"
    elif score >= 20:
        level = "🟡 주의"
    else:
        level = "🟢 안전"
    return score, level

def check_school_zone(dest_lat, dest_lng):
    warnings = []
    for zone in school_zones:
        distance = math.sqrt((zone["lat"] - dest_lat)**2 + (zone["lng"] - dest_lng)**2) * 111
        if distance <= 0.5:
            warnings.append(zone["name"])
    return warnings

def show_results(destination, vehicle_type, lang_code):
    t = lambda text: translate(text, lang_code)
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    params = {"query": destination + " 주차장", "size": 5}
    res = requests.get(url, headers=headers, params=params)
    docs = res.json().get("documents", [])
    if not docs:
        st.error(t("검색 결과가 없어요."))
        return
    first = docs[0]
    lat0 = float(first["y"])
    lng0 = float(first["x"])
    m = folium.Map(location=[lat0, lng0], zoom_start=14)
    st.subheader(t("📍 주변 주차장 위험도"))
    for p in docs:
        name = p["place_name"]
        lat = float(p["y"])
        lng = float(p["x"])
        score, level = calculate_danger_score(name, p["category_name"])
        color = "red" if score >= 50 else "orange" if score >= 20 else "green"
        st.write(f"{level} **{name}**")
        st.caption(f"{p['address_name']} | {t('위험점수')}: {score}점")
        folium.Marker([lat, lng], tooltip=f"{level} {name}", icon=folium.Icon(color=color)).add_to(m)
    st.subheader(t("🏫 어린이보호구역"))
    zone_warnings = check_school_zone(lat0, lng0)
    if zone_warnings:
        for w in zone_warnings:
            st.error(f"🔴 {t('경고')} - {w} | 30km/h")
    else:
        st.success(t("✅ 주변 어린이보호구역 없음"))
    st.subheader(t("🗺️ 추천 코스"))
    for c in courses:
        if vehicle_type in c["recommended_vehicle"]:
            with st.expander(f"✅ {t(c['name'])} | {t(c['difficulty'])} | {c['duration']}"):
                st.write(" → ".join([t(s) for s in c["spots"]]))
    st.subheader(t("🧭 네비게이션"))
    dest_name = docs[0]["place_name"]
    dest_lat = float(docs[0]["y"])
    dest_lng = float(docs[0]["x"])
    kakao_nav_url = f"kakaomap://route?ep={dest_lat},{dest_lng}&by=CAR"
    kakao_web_url = f"https://map.kakao.com/link/to/{dest_name},{dest_lat},{dest_lng}"
    st.markdown(f"""
        <a href="{kakao_nav_url}" style="
            display:inline-block;
            background:#FEE500;
            color:#000000;
            padding:12px 24px;
            border-radius:8px;
            font-weight:bold;
            text-decoration:none;
            margin-right:10px;
            font-size:16px;">
            📱 카카오맵 앱으로 네비게이션
        </a>
        <a href="{kakao_web_url}" target="_blank" style="
            display:inline-block;
            background:#0077B6;
            color:white;
            padding:12px 24px;
            border-radius:8px;
            font-weight:bold;
            text-decoration:none;
            font-size:16px;">
            🌐 웹에서 길찾기
        </a>
    """, unsafe_allow_html=True)
    st.subheader(t("🗾 지도"))
    st_folium(m, width=700, height=400)

st.set_page_config(page_title="KVanguard Drive", page_icon="🚗", layout="centered")
st.title("🚗 KVanguard Drive")
st.caption("외국인 렌터카 운전자를 위한 드라이빙 어시스턴트")

if "searched" not in st.session_state:
    st.session_state.searched = False

destination = st.text_input("📍 목적지", placeholder="예: 제주 성산일출봉")
vehicle_type = st.selectbox("🚙 차종", ["소형", "중형", "대형", "SUV"])
language = st.selectbox("🌐 언어", list(languages.keys()))
lang_code = languages[language]

if st.button("🔍 검색하기"):
    if not destination:
        st.warning("목적지를 입력해주세요!")
    else:
        st.session_state.searched = True
        st.session_state.dest = destination
        st.session_state.vehicle = vehicle_type
        st.session_state.lang = lang_code

if st.session_state.searched:
    show_results(st.session_state.dest, st.session_state.vehicle, st.session_state.lang)
