"fc59295141197b8cf11c0c47dfa5c92c"
import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import math
from deep_translator import GoogleTranslator

KAKAO_API_KEY = "fc59295141197b8cf11c0c47dfa5c92c"

# 한국적 세련된 디자인 CSS
STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', 'DM Sans', sans-serif;
}

.stApp {
    background-color: #F7F5F0;
}

.main-header {
    text-align: center;
    padding: 2rem 0 1rem 0;
}

.main-title {
    font-size: 2rem;
    font-weight: 700;
    color: #1a1a2e;
    letter-spacing: -0.5px;
}

.main-subtitle {
    font-size: 0.85rem;
    color: #888;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 4px;
}

.divider {
    width: 40px;
    height: 3px;
    background: #0077B6;
    margin: 12px auto;
    border-radius: 2px;
}

.card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 12px;
    border: 1px solid #efefef;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    transition: box-shadow 0.2s;
}

.card:hover {
    box-shadow: 0 4px 20px rgba(0,119,182,0.1);
}

.rental-card {
    background: white;
    border-radius: 16px;
    padding: 18px 20px;
    margin-bottom: 10px;
    border: 1px solid #efefef;
    text-decoration: none;
    display: block;
    color: #1a1a2e;
    transition: all 0.2s;
}

.rental-card:hover {
    border-color: #0077B6;
    box-shadow: 0 4px 20px rgba(0,119,182,0.12);
    transform: translateY(-1px);
}

.rental-name {
    font-weight: 600;
    font-size: 0.95rem;
    color: #1a1a2e;
}

.rental-desc {
    font-size: 0.8rem;
    color: #888;
    margin-top: 3px;
}

.tag {
    display: inline-block;
    background: #EBF5FB;
    color: #0077B6;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
    margin-top: 6px;
}

.vehicle-match {
    background: white;
    border-radius: 14px;
    padding: 16px 18px;
    margin-bottom: 10px;
    border-left: 3px solid #0077B6;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.vehicle-match-title {
    font-weight: 600;
    font-size: 0.95rem;
    color: #1a1a2e;
}

.vehicle-match-sub {
    font-size: 0.8rem;
    color: #888;
    margin-top: 2px;
}

.nav-btn {
    display: inline-block;
    padding: 12px 22px;
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.9rem;
    text-decoration: none;
    margin-right: 8px;
    margin-bottom: 8px;
    transition: opacity 0.2s;
}

.nav-btn:hover {
    opacity: 0.85;
}

.section-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #0077B6;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
    margin-top: 20px;
}

.danger-item {
    background: white;
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 8px;
    border: 1px solid #efefef;
    font-size: 0.9rem;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: white;
    border-radius: 12px;
    padding: 4px;
    border: 1px solid #efefef;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-weight: 500;
    font-size: 0.875rem;
    color: #888;
    padding: 8px 16px;
}

.stTabs [aria-selected="true"] {
    background: #0077B6 !important;
    color: white !important;
}

.stTextInput > div > div > input {
    border-radius: 10px;
    border: 1px solid #e0e0e0;
    padding: 10px 14px;
    font-family: 'Noto Sans KR', sans-serif;
    background: white;
}

.stSelectbox > div > div {
    border-radius: 10px;
    background: white;
}

.stButton > button {
    background: #0077B6;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 24px;
    font-weight: 600;
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 0.9rem;
    transition: background 0.2s;
}

.stButton > button:hover {
    background: #005f92;
}
</style>
"""

languages = {
    "한국어": "ko", "English": "en", "日本語": "ja", "中文(简体)": "zh-CN",
    "Español": "es", "Français": "fr", "Deutsch": "de", "Italiano": "it",
    "Português": "pt", "Русский": "ru", "العربية": "ar", "हिन्दी": "hi",
    "Bahasa Indonesia": "id", "Tiếng Việt": "vi", "ภาษาไทย": "th",
    "Türkçe": "tr", "Polski": "pl", "Nederlands": "nl", "Svenska": "sv",
    "Ελληνικά": "el", "Українська": "uk", "עברית": "he", "Swahili": "sw",
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
    st.caption(t("평소 몰던 차 이름을 입력하면 유사한 국내 차량을 찾아드려요"))
    foreign_search = st.text_input("", placeholder="예: Camry, Civic, RAV4, Golf", label_visibility="collapsed")
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
    category = st.selectbox("", ["소형", "중형", "대형", "SUV"], label_visibility="collapsed")
    car_list = vehicles[category]
    selected_car = st.selectbox("", list(car_list.keys()), label_visibility="collapsed", key="car_select")
    if selected_car:
        car_info = car_list[selected_car]
        st.markdown(f"""
        <div class="card">
            <div style="font-weight:600; color:#1a1a2e;">✅ {selected_car}</div>
            <div style="font-size:0.8rem; color:#888; margin-top:4px;">{t("유사 외국 차량")}: {', '.join(car_info['foreign'])}</div>
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
            with st.expander(f"✅ {t(c['name'])} · {t(c['difficulty'])} · {c['duration']}"):
                st.write(" → ".join([t(s) for s in c["spots"]]))

def show_navigation(destination, t):
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
            <span style="font-size:0.8rem; color:#888;">{p['address_name']}</span>
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
        <a href="{kakao_nav_url}" class="nav-btn" style="background:#FEE500; color:#1a1a2e;">📱 {t("카카오맵 네비게이션")}</a>
        <a href="{kakao_web_url}" target="_blank" class="nav-btn" style="background:#0077B6; color:white;">🌐 {t("웹에서 길찾기")}</a>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f'<div class="section-label">{t("지도")}</div>', unsafe_allow_html=True)
    st_folium(m, width=700, height=380)

# ── 메인 ─────────────────────────────────
st.set_page_config(page_title="KVanguard Drive", page_icon="🚗", layout="centered")
st.markdown(STYLE, unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <div class="main-title">🚗 KVanguard Drive</div>
    <div class="divider"></div>
    <div class="main-subtitle">Jeju Island · Drive Assistant</div>
</div>
""", unsafe_allow_html=True)

language = st.selectbox("", list(languages.keys()), label_visibility="collapsed")
lang_code = languages[language]
t = lambda text: translate(text, lang_code)

st.divider()

tab1, tab2, tab3 = st.tabs([t("🚗 렌트카"), t("🗺️ 드라이브"), t("🧭 네비게이션")])

with tab1:
    show_rental_tab(t)

with tab2:
    vehicle_type = st.session_state.get("nav_vehicle", "소형")
    vehicle_type = st.selectbox(t("차종"), ["소형", "중형", "대형", "SUV"],
        index=["소형", "중형", "대형", "SUV"].index(vehicle_type))
    show_courses(vehicle_type, t)

with tab3:
    destination = st.text_input("", placeholder=t("목적지 입력 (예: 제주 성산일출봉)"), label_visibility="collapsed")
    if st.button(t("검색하기")):
        if not destination:
            st.warning(t("목적지를 입력해주세요!"))
        else:
            st.session_state.nav_dest = destination
    if "nav_dest" in st.session_state:
        show_navigation(st.session_state.nav_dest, t)
