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

# ── 차량 데이터 ──────────────────────────
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

# ── 렌트카 업체 데이터 ────────────────────
rental_info = {
    "제주렌트카": {"url": "https://www.jejurentcar.co.kr", "desc": "1978년 창립 국내 1호, 공항 셔틀 1분"},
    "제주엔젤카": {"url": "https://www.jejuangeltour.com", "desc": "완전자차 무료, 우수관광사업체"},
    "제주원렌트카": {"url": "https://www.jejuonecar.kr", "desc": "최대 94% 할인, 24시간 무료취소"},
    "롯데렌터카": {"url": "https://www.lotterentacar.net/hp/kor/reservation/index.do?state=2&rentArea=6", "desc": "제주 웰컴 쿠폰팩 제공"},
    "조아렌트카": {"url": "https://www.joarent.com", "desc": "즉시 예약 확정, 가성비 최고"},
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
                    results.append({
                        "category": category,
                        "korean_name": korean_name,
                        "foreign_name": foreign_name,
                        "rental": info["rental"]
                    })
    return results

def show_rental_tab(t):
    st.subheader(t("🚗 렌트카 예약"))

    # 자국 차량 검색
    st.markdown(f"#### {t('🔍 자국 차량으로 검색')}")
    st.caption(t("평소 몰던 차 이름을 영어로 입력하면 유사한 국내 차량을 찾아드려요!"))
    foreign_search = st.text_input(t("차량 검색"), placeholder="예: Camry, Civic, RAV4, Golf")

    if foreign_search:
        found = find_vehicle_by_foreign(foreign_search)
        if found:
            st.success(t(f"'{foreign_search}' 와 유사한 차량을 찾았어요!"))
            for f in found:
                st.markdown(f"""
                    <div style="background:#f0f8ff; border:1px solid #0077B6; border-radius:12px; padding:14px; margin-bottom:10px;">
                        <b>🚗 {f['foreign_name']} → {f['korean_name']}</b>
                        <span style="background:#0077B6; color:white; padding:2px 8px; border-radius:10px; font-size:12px; margin-left:8px;">{t(f['category'])}</span>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown(t("**예약 가능 업체:**"))
                for r in f["rental"]:
                    info = rental_info[r]
                    st.markdown(f"""
                        <a href="{info['url']}" target="_blank" style="
                            display:block;
                            background:#ffffff;
                            border:1px solid #dee2e6;
                            border-radius:8px;
                            padding:10px 14px;
                            margin-bottom:6px;
                            text-decoration:none;
                            color:#000000;">
                            🏢 <b>{r}</b> — {t(info['desc'])}
                        </a>
                    """, unsafe_allow_html=True)
                st.divider()
        else:
            st.warning(t(f"'{foreign_search}' 와 유사한 차량을 찾지 못했어요. 아래에서 직접 선택해주세요."))

    st.markdown(f"#### {t('🚙 차종으로 직접 선택')}")
    category = st.selectbox(t("차종 선택"), ["소형", "중형", "대형", "SUV"])
    car_list = vehicles[category]
    selected_car = st.selectbox(t("세부 차량 선택"), list(car_list.keys()))

    if selected_car:
        car_info = car_list[selected_car]
        st.info(t(f"✅ {selected_car} 선택됨"))
        st.caption(t(f"유사 외국 차량: {', '.join(car_info['foreign'])}"))
        st.markdown(t("**예약 가능 업체:**"))
        for r in car_info["rental"]:
            info = rental_info[r]
            st.markdown(f"""
                <a href="{info['url']}" target="_blank" style="
                    display:block;
                    background:#f0f8ff;
                    border:1px solid #0077B6;
                    border-radius:12px;
                    padding:14px 18px;
                    margin-bottom:8px;
                    text-decoration:none;
                    color:#000000;">
                    🏢 <b>{r}</b><br>
                    <span style="color:#555; font-size:14px;">{t(info['desc'])}</span>
                </a>
            """, unsafe_allow_html=True)
        if "nav_vehicle" not in st.session_state:
            st.session_state.nav_vehicle = category
        st.session_state.nav_vehicle = category

def show_courses(vehicle_type, t):
    st.subheader(t("🗺️ 추천 드라이브 코스"))
    for c in courses:
        if vehicle_type in c["recommended_vehicle"]:
            with st.expander(f"✅ {t(c['name'])} | {t(c['difficulty'])} | {c['duration']}"):
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
    st.subheader(t("🧭 네비게이션"))
    dest_name = docs[0]["place_name"]
    dest_lat = float(docs[0]["y"])
    dest_lng = float(docs[0]["x"])
    kakao_nav_url = f"kakaomap://route?ep={dest_lat},{dest_lng}&by=CAR"
    kakao_web_url = f"https://map.kakao.com/link/to/{dest_name},{dest_lat},{dest_lng}"
    st.markdown(f"""
        <a href="{kakao_nav_url}" style="
            display:inline-block; background:#FEE500; color:#000000;
            padding:12px 24px; border-radius:8px; font-weight:bold;
            text-decoration:none; margin-right:10px; font-size:16px;">
            📱 카카오맵 앱으로 네비게이션
        </a>
        <a href="{kakao_web_url}" target="_blank" style="
            display:inline-block; background:#0077B6; color:white;
            padding:12px 24px; border-radius:8px; font-weight:bold;
            text-decoration:none; font-size:16px;">
            🌐 웹에서 길찾기
        </a>
    """, unsafe_allow_html=True)
    st.subheader(t("🗾 지도"))
    st_folium(m, width=700, height=400)

# ── 메인 UI ──────────────────────────────
st.set_page_config(page_title="KVanguard Drive", page_icon="🚗", layout="centered")
st.title("🚗 KVanguard Drive")
st.caption("제주도 외국인 렌터카 드라이빙 어시스턴트")

language = st.selectbox("🌐 언어 / Language", list(languages.keys()))
lang_code = languages[language]
t = lambda text: translate(text, lang_code)

st.divider()

tab1, tab2, tab3 = st.tabs([
    t("🚗 렌트카 예약"),
    t("🗺️ 드라이브 코스"),
    t("🧭 네비게이션")
])

with tab1:
    show_rental_tab(t)

with tab2:
    vehicle_type = st.session_state.get("nav_vehicle", "소형")
    vehicle_type = st.selectbox(t("🚙 차종"), ["소형", "중형", "대형", "SUV"],
        index=["소형", "중형", "대형", "SUV"].index(vehicle_type))
    show_courses(vehicle_type, t)

with tab3:
    destination = st.text_input(t("📍 목적지 입력"), placeholder="예: 제주 성산일출봉")
    if st.button(t("🔍 검색하기")):
        if not destination:
            st.warning(t("목적지를 입력해주세요!"))
        else:
            st.session_state.nav_dest = destination
    if "nav_dest" in st.session_state:
        show_navigation(st.session_state.nav_dest, t)
