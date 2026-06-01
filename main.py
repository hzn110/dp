import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# 기본 설정
# -------------------------

st.set_page_config(
    page_title="Game Server Cooling Cost Predictor",
    page_icon="🎮",
    layout="wide"
)

# -------------------------
# 데이터 불러오기
# -------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("ta_20260601093156.csv")

    df["날짜"] = pd.to_datetime(df["날짜"])

    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month

    return df

df = load_data()

monthly_avg = (
    df.groupby("월")["평균기온(℃)"]
    .mean()
)

# -------------------------
# 사이드바 메뉴
# -------------------------

menu = st.sidebar.radio(
    "메뉴 선택",
    [
        "홈",
        "기온 분석",
        "서버 운영 시뮬레이션",
        "운영 비용 예측"
    ]
)

# -------------------------
# HOME
# -------------------------

if menu == "홈":

    st.title("🎮 게임 서버 운영 비용 예측기")

    st.markdown("""
    ## 프로젝트 소개

    1980~2026년 기온 데이터를 활용하여

    - 월별 평균 기온 분석
    - 서버 냉각 부담 분석
    - 게임 서버 운영 비용 예측

    을 수행하는 시스템입니다.
    """)

    st.info("""
    데이터 출처:
    1980~2026 기온 데이터
    """)

# -------------------------
# 기온 분석
# -------------------------

elif menu == "기온 분석":

    st.title("📈 기온 데이터 분석")

    chart_df = (
        df.groupby("월")["평균기온(℃)"]
        .mean()
        .reset_index()
    )

    fig = px.line(
        chart_df,
        x="월",
        y="평균기온(℃)",
        markers=True,
        title="1980~2026 월별 평균 기온"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(chart_df)

# -------------------------
# 서버 운영 시뮬레이션
# -------------------------

elif menu == "서버 운영 시뮬레이션":

    st.title("🖥 서버 운영 시뮬레이션")

    month = st.selectbox(
        "운영 월",
        range(1, 13)
    )

    server_count = st.number_input(
        "서버 수",
        min_value=1,
        value=20
    )

    power_per_server = st.number_input(
        "서버 1대 소비전력(W)",
        min_value=100,
        value=500
    )

    outside_temp = monthly_avg.loc[month]

    total_power = (
        server_count *
        power_per_server
    )

    st.metric(
        "평균 외기온",
        f"{outside_temp:.1f} ℃"
    )

    st.metric(
        "총 소비전력",
        f"{total_power:,} W"
    )

    if outside_temp < 15:
        level = "낮음 🟢"

    elif outside_temp < 25:
        level = "보통 🟡"

    else:
        level = "높음 🔴"

    st.success(
        f"예상 냉각 부담: {level}"
    )

# -------------------------
# 운영 비용 예측
# -------------------------

elif menu == "운영 비용 예측":

    st.title("💰 운영 비용 예측")

    month = st.selectbox(
        "운영 월",
        range(1, 13)
    )

    server_count = st.number_input(
        "서버 수",
        min_value=1,
        value=50
    )

    power_per_server = st.number_input(
        "서버 1대 소비전력(W)",
        min_value=100,
        value=500
    )

    electric_rate = st.number_input(
        "전기요금 (원/kWh)",
        min_value=50,
        value=150
    )

    outside_temp = monthly_avg.loc[month]

    power_kw = (
        server_count *
        power_per_server
    ) / 1000

    monthly_usage = (
        power_kw *
        24 *
        30
    )

    server_cost = (
        monthly_usage *
        electric_rate
    )

    cooling_cost = (
        server_cost *
        (outside_temp / 100)
    )

    total_cost = (
        server_cost +
        cooling_cost
    )

    st.metric(
        "서버 전력 비용",
        f"{server_cost:,.0f} 원"
    )

    st.metric(
        "냉각 비용",
        f"{cooling_cost:,.0f} 원"
    )

    st.metric(
        "총 운영 비용",
        f"{total_cost:,.0f} 원"
    )

    if outside_temp >= 25:
        st.error(
            "여름철 냉각 비용 증가 예상"
        )

    else:
        st.success(
            "냉각 비용 안정적"
        )
