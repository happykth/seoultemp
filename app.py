import streamlit as st
import pandas as pd

st.set_page_config(page_title="서울 기온 데이터", page_icon="🌡️", layout="centered")

# ---------- 스타일 (따뜻한 색감) ----------
st.markdown("""
<style>
.stApp {
    background-color: #FFF8F0;
}
h1, h2, h3 {
    color: #C15C2B;
}
div[data-testid="stMetric"] {
    background-color: #FFEEDD;
    border: 1px solid #F3C9A0;
    border-radius: 12px;
    padding: 12px 8px;
}
div[data-testid="stMetricLabel"] {
    color: #A8481B;
}
</style>
""", unsafe_allow_html=True)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"

st.title("🌡️ 서울 기온 데이터 살펴보기")
st.caption(f"데이터 출처: {DATA_URL}")


@st.cache_data
def load_data(url: str) -> pd.DataFrame:
    df = pd.read_csv(url, encoding="utf-8-sig")
    return df


with st.spinner("데이터를 불러오는 중이에요..."):
    df = load_data(DATA_URL)

# 기온 관련 컬럼 자동 탐색 (평균/최고/최저기온 컬럼명이 다를 수 있어 유연하게 매칭)
temp_col_candidates = {
    "평균": [c for c in df.columns if "평균" in c and "기온" in c],
    "최고": [c for c in df.columns if "최고" in c and "기온" in c],
    "최저": [c for c in df.columns if "최저" in c and "기온" in c],
}

st.subheader("📋 데이터 앞부분 미리보기")
st.dataframe(df.head(), use_container_width=True)

st.subheader("📊 요약 통계")

avg_col = temp_col_candidates["평균"][0] if temp_col_candidates["평균"] else None
max_col = temp_col_candidates["최고"][0] if temp_col_candidates["최고"] else None
min_col = temp_col_candidates["최저"][0] if temp_col_candidates["최저"] else None

col1, col2, col3, col4 = st.columns(4)

col1.metric("관측 개수", f"{len(df):,} 건")

if avg_col:
    col2.metric("평균 기온", f"{df[avg_col].mean():.1f} ℃")
else:
    col2.metric("평균 기온", "컬럼 없음")

if max_col:
    col3.metric("최고 기온", f"{df[max_col].max():.1f} ℃")
else:
    col3.metric("최고 기온", "컬럼 없음")

if min_col:
    col4.metric("최저 기온", f"{df[min_col].min():.1f} ℃")
else:
    col4.metric("최저 기온", "컬럼 없음")

st.subheader("🕳️ 열별 결측치(관측 없는 날) 개수")
missing_df = df.isna().sum().reset_index()
missing_df.columns = ["열(컬럼)", "결측치 개수"]
missing_df["결측 비율(%)"] = (missing_df["결측치 개수"] / len(df) * 100).round(2)
st.dataframe(missing_df, use_container_width=True, hide_index=True)

with st.expander("전체 컬럼 통계 자세히 보기 (describe)"):
    st.dataframe(df.describe(), use_container_width=True)

with st.expander("전체 컬럼명 확인"):
    st.write(list(df.columns))
