import streamlit as st
import random
import pandas as pd

st.set_page_config(
    page_title="AI 식단 추천 앱",
    page_icon="🥗",
    layout="wide"
)

st.title("🥗 AI 식단 추천 앱")
st.write("냉장고 재료를 입력하면 식단을 추천해드립니다!")

# 음식 데이터
meal_db = [
    {
        "name": "닭가슴살 샐러드",
        "ingredients": ["닭가슴살", "양상추", "토마토"],
        "calories": 320,
        "difficulty": "쉬움"
    },
    {
        "name": "김치볶음밥",
        "ingredients": ["김치", "밥", "계란"],
        "calories": 550,
        "difficulty": "쉬움"
    },
    {
        "name": "토마토 파스타",
        "ingredients": ["토마토", "파스타면", "양파"],
        "calories": 670,
        "difficulty": "보통"
    },
    {
        "name": "계란말이",
        "ingredients": ["계란", "당근", "양파"],
        "calories": 280,
        "difficulty": "쉬움"
    },
    {
        "name": "소고기 덮밥",
        "ingredients": ["소고기", "양파", "밥"],
        "calories": 720,
        "difficulty": "보통"
    },
]

# 사용자 입력
st.sidebar.header("🥕 냉장고 재료 입력")

user_input = st.sidebar.text_area(
    "재료를 쉼표(,)로 구분해서 입력하세요",
    placeholder="예: 계란, 양파, 김치"
)

meal_type = st.sidebar.selectbox(
    "식사 종류",
    ["아침", "점심", "저녁"]
)

recommend_btn = st.sidebar.button("식단 추천받기")

# 추천 알고리즘
if recommend_btn:

    user_ingredients = [
        x.strip() for x in user_input.split(",")
    ]

    recommendations = []

    for meal in meal_db:

        matched = set(user_ingredients) & set(meal["ingredients"])

        if len(matched) >= 1:
            recommendations.append({
                "메뉴": meal["name"],
                "일치 재료 수": len(matched),
                "칼로리": meal["calories"],
                "난이도": meal["difficulty"],
                "사용 재료": ", ".join(meal["ingredients"])
            })

    st.subheader(f"🍽️ {meal_type} 추천 식단")

    if recommendations:

        recommendations = sorted(
            recommendations,
            key=lambda x: x["일치 재료 수"],
            reverse=True
        )

        for item in recommendations:

            with st.container():

                st.markdown(f"## 🍴 {item['메뉴']}")

                col1, col2, col3 = st.columns(3)

                col1.metric("칼로리", f"{item['칼로리']} kcal")
                col2.metric("난이도", item["난이도"])
                col3.metric("일치 재료", item["일치 재료 수"])

                st.write(f"**사용 재료:** {item['사용 재료']}")

                st.progress(min(item["일치 재료 수"] / 3, 1.0))

                st.divider()

    else:
        st.warning("추천 가능한 식단이 없습니다 😢")
        st.write("다른 재료를 추가해보세요!")

# 랜덤 건강 팁
tips = [
    "🥦 채소를 하루 500g 이상 섭취해보세요!",
    "💧 물을 충분히 마시면 포만감 유지에 도움됩니다.",
    "🍎 과일은 간식으로 좋아요!",
    "🏃 식사 후 가벼운 산책을 추천합니다."
]

st.sidebar.divider()
st.sidebar.info(random.choice(tips))
