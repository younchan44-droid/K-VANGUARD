import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import math
from deep_translator import GoogleTranslator
import os
from PIL import Image

KAKAO_API_KEY = "7367cff3f01358d90a9dd5af3f67ca54"

# 고품격 전통 한옥 & 모던 프리미엄 스타일링 (Concept 2 완전 매칭)
STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&family=Outfit:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] {
    font-family: 'Outfit', 'Noto Sans KR', sans-serif;
}
.stApp {
    background-color: #F6F5F2; /* 기품 있는 은은한 전통 백자색 느낌의 웜그레이 */
    color: #2D3748;
}
/* 메인 프리미엄 헤더 카드 */
.main-header {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 3rem 2rem;
    margin-bottom: 2.5rem;
    border: 1px solid #EAE8E4;
    border-top: 6px solid #1E3047; /* 한옥 기와 선율을 형상화한 로열 인디고 탑 보더 */
    box-shadow: 0 12px 36px rgba(30, 48, 71, 0.05);
    text-align: center;
    position: relative;
    overflow: hidden;
}
/* 기와 물받이 또는 은은한 전통 문양 데코를 연상시키는 배경 요소 */
.main-header::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: repeating-linear-gradient(45deg, #1E3047, #1E3047 10px, #C84B4B 10px, #C84B4B 20px);
    opacity: 0.8;
}
.main-title {
    font-size: 2.4rem;
    font-weight: 700;
    color: #1E3047;
    letter-spacing: -0.5px;
    margin: 0;
}
.main-subtitle {
    font-size: 0.95rem;
    color: #C84B4B; /* 한국적 전통 연지색 (홍색) */
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 10px;
}
.divider {
    width: 80px;
    height: 4px;
    background: linear-gradient(90deg, #1E3047 0%, #C84B4B 100%);
    margin: 18px auto;
    border-radius: 2px;
}
/* 검색창 텍스트 색상 안보이는 버그 전면 해결 & 인풋창 프리미엄 스타일링 */
.stTextInput input {
    color: #1E3047 !important; /* 글자색을 명확한 어두운 인디고로 지정 */
    background-color: #FFFFFF !important;
    border: 2px solid #E2E8F0 !important;
    border-radius: 12px !important;
    padding: 14px 18px !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    transition: all 0.25s ease !important;
}
.stTextInput input:focus {
    border-color: #1E3047 !important;
    box-shadow: 0 0 0 4px rgba(30, 48, 71, 0.12) !important;
    background-color: #FFFFFF !important;
}
.stTextInput input::placeholder {
    color: #A0AEC0 !important;
}
/* 셀렉트박스 고품격 스타일링 */
.stSelectbox > div > div {
    background-color: #FFFFFF !important;
    border: 2px solid #E2E8F0 !important;
    border-radius: 12px !important;
    color: #1E3047 !important;
    transition: all 0.25s ease !important;
}
.stSelectbox > div > div:focus-within {
    border-color: #1E3047 !important;
    box-shadow: 0 0 0 4px rgba(30, 48, 71, 0.12) !important;
}
/* 입력창 상단 라벨 텍스트 프리미엄 시각화 (가독성 문제 해결) */
.stTextInput label, .stSelectbox label {
    color: #1E3047 !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    margin-bottom: 8px !important;
    display: inline-block !important;
    letter-spacing: -0.3px !important;
}
/* 정보 표시 카드(Card) 스타일링 업그레이드 */
.card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    border: 1px solid #EAE8E4;
    border-left: 5px solid #1E3047; /* 인디고 좌측 포인트 바 */
    box-shadow: 0 6px 16px rgba(30, 48, 71, 0.02);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.card:hover {
    box-shadow: 0 12px 30px rgba(30, 48, 71, 0.08);
    transform: translateY(-3px);
}
/* 렌트카 업체 카드 스타일링 업그레이드 */
.rental-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 14px;
    border: 1px solid #EAE8E4;
    border-left: 5px solid #C84B4B; /* 연지색(홍색) 좌측 포인트 바 */
    text-decoration: none;
    display: block;
    color: #2D3748;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 10px rgba(30, 48, 71, 0.02);
}
.rental-card:hover {
    border-color: #C84B4B;
    box-shadow: 0 12px 28px rgba(200, 75, 75, 0.1);
    transform: translateY(-3px);
}
.rental-name {
    font-weight: 700;
    font-size: 1.05rem;
    color: #1E3047;
}
.rental-desc {
    font-size: 0.88rem;
    color: #718096;
    margin-top: 6px;
}
.tag {
    display: inline-block;
    background: #F8F9FA;
    color: #1E3047;
    border: 1px solid #E2E8F0;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 700;
    margin-top: 8px;
}
/* 차량 매칭 결과 카드 디자인 업그레이드 */
.vehicle-match {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 16px;
    border: 1px solid #EAE8E4;
    border-top: 4px solid #1E3047;
    box-shadow: 0 6px 18px rgba(30, 48, 71, 0.03);
}
.vehicle-match-title {
    font-weight: 800;
    font-size: 1.1rem;
    color: #1E3047;
}
.vehicle-match-sub {
    font-size: 0.9rem;
    color: #718096;
    margin-top: 6px;
}
/* 네비게이션 버튼 디자인 업그레이드 */
.nav-btn {
    display: inline-block;
    padding: 14px 26px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 0.95rem;
    text-decoration: none;
    margin-right: 10px;
    margin-bottom: 10px;
    transition: all 0.25s ease;
}
.nav-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.12);
}
.section-label {
    font-size: 0.85rem;
    font-weight: 800;
    color: #1E3047;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 12px;
    margin-top: 30px;
    border-left: 3px solid #C84B4B;
    padding-left: 10px;
}
.danger-item {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 12px;
    border: 1px solid #EAE8E4;
    font-size: 0.98rem;
    box-shadow: 0 4px 10px rgba(0,0,0,0.01);
}
/* 탭메뉴(Tabs) 명품 브랜딩 화 */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: #FFFFFF;
    border-radius: 16px;
    padding: 8px;
    border: 1px solid #EAE8E4;
    box-shadow: 0 4px 12px rgba(30, 48, 71, 0.02);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 12px;
    font-weight: 700;
    font-size: 0.95rem;
    color: #718096;
    padding: 12px 24px;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.stTabs [data-baseweb="tab"]:hover {
    color: #1E3047;
    background: #F7F6F3;
}
.stTabs [aria-selected="true"] {
    background: #1E3047 !important;
    color: #FFFFFF !important;
    box-shadow: 0 6px 16px rgba(30, 48, 71, 0.25);
}
/* 버튼 스타일링 극대화 */
.stButton > button {
    background: #1E3047;
    color: #FFFFFF;
    border: none;
    border-radius: 12px;
    padding: 14px 32px;
    font-weight: 700;
    font-size: 1rem;
    transition: all 0.25s ease-in-out;
    box-shadow: 0 6px 18px rgba(30, 48, 71, 0.15);
    width: 100%; /* 검색 버튼의 가시성을 위해 너비 100% 적용 */
}
.stButton > button:hover {
    background: #121E2E;
    color: #FFFFFF;
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(30, 48, 71, 0.25);
}
</style>
"""
languages = {
    "한국어": "ko", "English": "en", "日本語": "ja", "中文(简体)": "zh-CN",
    "Español": "es", "Français": "fr", "Deutsch": "de", "Italiano": "it",
    "Português": "pt", "Русский": "ru", "العربية": "ar", "हिन्दी": "hi",
    "Bahasa Indonesia": "id", "Tiếng Việt": "vi", "ภาษาไทย": "th",
    "Türkçe": "tr", "Polski": "pl", "Nederlands": "nl", "Svenska": "sv",
    "Ελληνικά": "el", "Ukranian": "uk", "Hebrew": "he", "Swahili": "sw",
}
vehicles = {
    "소형": {
        "아반떼": {"foreign": ["Civic", "Corolla", "Golf", "Focus", "Mazda3"], "rental": ["제주렌트카", "조아렌트카", "제주원렌트카"]},
        "모닝": {"foreign": ["Fit", "Yaris", "Polo", "Swift", "Jazz"], "rental": ["조아렌트카", "제주원렌트카"]},
        "레이": {"foreign": ["N-Box", "Tanto", "Spacia"], "rental": ["제주렌트카", "조아렌트카"]},
        "캐스퍼": {"foreign": ["Aqua", "Fit", "Vitz"], "rental": ["제주원렌트카", "조아렌트카"]},
    },
    "중형": {
        "쏘나타": {"foreign": ["Camry", "Accord", "Passat", "Mondeo", "Mazda6"], "rental": ["롯데렌터카", "제주렌트카", "제주엔젤카"]},
        "K5": {"foreign": ["Camry", "Accord", "Altima", "Fusion"], "rental": ["롯데렌터카", "제주엔젤카"]},
        "SM6": {"foreign": ["Megane", "Laguna", "Passat"], "rental": ["제주렌트카", "제주엔젤카"]},
    },
    "대형": {
        "그랜저": {"foreign": ["Avalon", "Maxima", "A6", "E-Class", "5 Series"], "rental": ["롯데렌터카", "제주엔젤카"]},
        "K8": {"foreign": ["Avalon", "Genesis", "A6"], "rental": ["롯데렌터카"]},
        "제네시스 G80": {"foreign": ["BMW 5 Series", "Mercedes E-Class", "Audi A6"], "rental": ["롯데렌터카", "제주엔젤카"]},
    },
    "SUV": {
        "투싼": {"foreign": ["CR-V", "RAV4", "Tiguan", "CX-5", "Forester"], "rental": ["제주렌트카", "제주엔젤카", "조아렌트카"]},
        "싼타페": {"foreign": ["Pilot", "Highlander", "Sorento", "Outlander"], "rental": ["롯데렌터카", "제주렌트카", "제주엔젤카"]},
        "팰리세이드": {"foreign": ["Pilot", "Highlander", "Traverse", "Pathfinder"], "rental": ["롯데렌터카", "제주엔젤카"]},
        "EV6": {"foreign": ["Tesla Model 3", "Ioniq 5", "BYD Han"], "rental": ["제주엔젤카", "제주원렌트카"]},
    },
}
rental_info = {
    "제주렌트카": {"url": "https://www.jejurentcar.co.kr", "desc": "1978년 창립 국내 1호"},
    "제주엔젤카": {"url": "https://www.jejuangeltour.com", "desc": "완전자차 무료"},
    "제주원렌트카": {"url": "https://www.jejuonecar.kr", "desc": "최대 94% 할인"},
    "롯데렌터카": {"url": "https://www.lotterentacar.net/hp/kor/reservation/index.do?state=2&rentArea=6", "desc": "웰컴 쿠폰팩 제공"},
    "조아렌트카": {"url": "https://www.joarent.com", "desc": "즉시 예약 확정"},
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
        level = "🔴 위험 (Mechanical/School Zone)"
    elif score >= 20:
        level = "🟡 주의 (Caution)"
    else:
        level = "🟢 안전 (Safe)"
    return score, level
def check_school_zone(dest_lat, dest_lng):
    warnings = []
    for zone in school_zones:
        distance = math.sqrt((zone["lat"] - dest_lat)**2 + (zone["lng"] - dest_lng)**2) * 111
        if distance <= 0.5:
            warnings.append(zone["name"])
    return warnings
def find_vehicle_by_foreign(search_term):
    results = []
    search_lower = search_term.lower()
    for category, car_list in vehicles.items():
        for korean_name, info in car_list.items():
            for foreign_name in info["foreign"]:
                if search_lower in foreign_name.lower():
                    results.append({"category": category, "korean_name": korean_name, "foreign_name": foreign_name, "rental": info["rental"]})
    return results
def show_rental_tab(t):
    st.markdown(f'<div class="section-label">{t("자국 차량으로 검색")}</div>', unsafe_allow_html=True)
    
    # 텍스트 입력창 라벨 명확하게 활성화
    foreign_search = st.text_input(
        label=t("평소 운전하시던 외산 차종을 입력하세요 (유사 국내 차량 추천)"), 
        placeholder="예: Camry, Civic, RAV4, Golf"
    )
    
    if foreign_search:
        found = find_vehicle_by_foreign(foreign_search)
        if found:
            for f in found:
                st.markdown(f"""
                <div class="vehicle-match">
                    <div class="vehicle-match-title">🚗 {f['foreign_name']} → {f['korean_name']} <span class="tag">{t(f['category'])}</span></div>
                    <div class="vehicle-match-sub">{t("예약 가능 업체")}</div>
                </div>
                """, unsafe_allow_html=True)
                for r in f["rental"]:
                    info = rental_info[r]
                    st.markdown(f"""
                    <a href="{info['url']}" target="_blank" class="rental-card">
                        <div class="rental-name">🏢 {r}</div>
                        <div class="rental-desc">{t(info['desc'])}</div>
                    </a>
                    """, unsafe_allow_html=True)
        else:
            st.warning(t(f"'{foreign_search}' 와 유사한 차량을 찾지 못했어요. 아래에서 직접 선택해주세요."))
    st.markdown(f'<div class="section-label">{t("차종으로 직접 선택")}</div>', unsafe_allow_html=True)
    
    category = st.selectbox(
        label=t("1단계: 원하시는 국내 차종 분류를 선택하세요"), 
        options=["소형", "중형", "대형", "SUV"]
    )
    
    car_list = vehicles[category]
    
    selected_car = st.selectbox(
        label=t("2단계: 대여 가능한 세부 차량을 선택하세요"), 
        options=list(car_list.keys()), 
        key="car_select"
    )
    
    if selected_car:
        car_info = car_list[selected_car]
        st.markdown(f"""
        <div class="card">
            <div style="font-weight:700; color:#1E3047; font-size: 1.1rem;">✅ {selected_car}</div>
            <div style="font-size:0.9rem; color:#718096; margin-top:6px;">{t("유사 외국 차량")}: {', '.join(car_info['foreign'])}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="section-label">{t("예약 가능 업체")}</div>', unsafe_allow_html=True)
        for r in car_info["rental"]:
            info = rental_info[r]
            st.markdown(f"""
            <a href="{info['url']}" target="_blank" class="rental-card">
                <div class="rental-name">🏢 {r}</div>
                <div class="rental-desc">{t(info['desc'])}</div>
            </a>
            """, unsafe_allow_html=True)
        st.session_state.nav_vehicle = category
def show_courses(vehicle_type, t):
    st.markdown(f'<div class="section-label">{t("추천 드라이브 코스")}</div>', unsafe_allow_html=True)
    for c in courses:
        if vehicle_type in c["recommended_vehicle"]:
            with st.expander(f"📌 {t(c['name'])} · {t(c['difficulty'])} · {c['duration']}"):
                st.write(" → ".join([t(s) for s in c["spots"]]))
def show_navigation(destination, t):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    params = {"query": destination + " 주차장", "size": 5}
    try:
        res = requests.get(url, headers=headers, params=params)
        docs = res.json().get("documents", [])
    except Exception:
        docs = []
        
    if not docs:
        st.error(t("검색 결과가 없어요. Kakao API Key가 올바른지 확인해주세요."))
        return
    first = docs[0]
    lat0 = float(first["y"])
    lng0 = float(first["x"])
    m = folium.Map(location=[lat0, lng0], zoom_start=14, tiles="CartoDB positron")
    st.markdown(f'<div class="section-label">{t("주변 주차장 위험도")}</div>', unsafe_allow_html=True)
    for p in docs:
        name = p["place_name"]
        lat = float(p["y"])
        lng = float(p["x"])
        score, level = calculate_danger_score(name, p["category_name"])
        color = "red" if score >= 50 else "orange" if score >= 20 else "green"
        st.markdown(f"""
        <div class="danger-item">
            {level} <b>{name}</b><br>
            <span style="font-size:0.9rem; color:#718096;">{p['address_name']}</span>
        </div>
        """, unsafe_allow_html=True)
        folium.Marker([lat, lng], tooltip=f"{level} {name}", icon=folium.Icon(color=color)).add_to(m)
    zone_warnings = check_school_zone(lat0, lng0)
    if zone_warnings:
        for w in zone_warnings:
            st.error(f"🔴 {t('경고')} — {w} | 30km/h")
    else:
        st.success(t("✅ 주변 어린이보호구역 없음"))
    dest_name = docs[0]["place_name"]
    dest_lat = float(docs[0]["y"])
    dest_lng = float(docs[0]["x"])
    kakao_nav_url = f"kakaomap://route?ep={dest_lat},{dest_lng}&by=CAR"
    kakao_web_url = f"https://map.kakao.com/link/to/{dest_name},{dest_lat},{dest_lng}"
    st.markdown(f"""
    <div style="margin: 16px 0;">
        <a href="{kakao_nav_url}" class="nav-btn" style="background:#FEE500; color:#1E3047; box-shadow: 0 4px 10px rgba(254, 229, 0, 0.3);">📱 {t("카카오맵 네비게이션")}</a>
        <a href="{kakao_web_url}" target="_blank" class="nav-btn" style="background:#1E3047; color:white;">🌐 {t("웹에서 길찾기")}</a>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f'<div class="section-label">{t("지도")}</div>', unsafe_allow_html=True)
    st_folium(m, width=700, height=380)
# ── 메인 실행 ───────────────────────────
icon_image = "🚗"
if os.path.exists("korean_simple_icon_compressed.png"):
    try:
        icon_image = Image.open("korean_simple_icon_compressed.png")
    except Exception:
        pass
st.set_page_config(page_title="KVanguard Drive", page_icon=icon_image, layout="centered")
st.markdown(STYLE, unsafe_allow_html=True)
# 한국의 아름다운 브랜드 가치를 전달하는 프리미엄 헤더 구성
st.markdown("""
<div class="main-header">
    <div class="main-title">KVanguard Drive</div>
    <div class="divider"></div>
    <div class="main-subtitle">Jeju Island · Premium Drive Assistant</div>
</div>
""", unsafe_allow_html=True)
# 다국어 번역 언어 선택 상자 라벨화 및 스타일링
language = st.selectbox(
    label="🌎 Select Language / 언어 선택", 
    options=list(languages.keys())
)
lang_code = languages[language]
t = lambda text: translate(text, lang_code)
st.divider()
tab1, tab2, tab3 = st.tabs([t("🚗 렌트카 예약"), t("🗺️ 코스 탐색"), t("🧭 목적지 안내")])
with tab1:
    show_rental_tab(t)
with tab2:
    vehicle_type = st.session_state.get("nav_vehicle", "소형")
    vehicle_type = st.selectbox(
        label=t("현재 선택된 차종 (차종에 알맞은 드라이브 코스가 자동 활성화됩니다)"), 
        options=["소형", "중형", "대형", "SUV"],
        index=["소형", "중형", "대형", "SUV"].index(vehicle_type)
    )
    show_courses(vehicle_type, t)
with tab3:
    destination = st.text_input(
        label=t("제주 관광 명소 혹은 주차장 검색"), 
        placeholder=t("예: 제주 성산일출봉, 협재해수욕장")
    )
    if st.button(t("목적지 검색 실행")):
        if not destination:
            st.warning(t("목적지를 입력해주세요!"))
        else:
            st.session_state.nav_dest = destination
    if "nav_dest" in st.session_state:
        show_navigation(st.session_state.nav_dest, t)

