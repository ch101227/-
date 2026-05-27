# app.py

import streamlit as st
from google import genai
from google.genai import types

# =========================
# 페이지 설정
# =========================
st.set_page_config(
    page_title="메뉴 추천 챗봇",
    page_icon="🍽️",
    layout="centered"
)

st.title("🍽️ AI 메뉴 추천 챗봇")
st.caption("오늘 뭐 먹을지 고민될 때 AI에게 물어보세요!")

# =========================
# Gemini 설정
# =========================
API_KEY = "AIzaSyCuZbTL4jytEEXFDbnLAy6H7EkEGmWR_cI"

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error(f"Gemini 클라이언트 초기화 실패: {e}")
    st.stop()

MODEL_NAME = "gemini-2.5-flash-lite"

SYSTEM_PROMPT = """
너는 음식 메뉴 추천 전문 AI 챗봇이다.

사용자의 상황, 기분, 날씨, 시간대, 예산, 선호 음식 등을 고려해서
먹기 좋은 메뉴를 추천해라.

응답 규칙:
- 친근하고 자연스럽게 말할 것
- 메뉴 추천 이유를 함께 설명할 것
- 가능하면 3개 이상 추천할 것
- 너무 길지 않게 답변할 것
"""

# =========================
# 세션 상태 초기화
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# 기존 채팅 출력
# =========================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# 사용자 입력
# =========================
user_input = st.chat_input("예: 오늘 비 오는데 따뜻한 음식 추천해줘")

if user_input:

    # 사용자 메시지 저장
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 생성
    with st.chat_message("assistant"):

        with st.spinner("메뉴 고민 중... 🍜"):

            try:
                # 이전 대화 기록 구성
                history_text = ""

                for msg in st.session_state.messages:
                    role = "사용자" if msg["role"] == "user" else "AI"
                    history_text += f"{role}: {msg['content']}\n"

                full_prompt = f"""
{SYSTEM_PROMPT}

아래는 이전 대화 기록이다.

{history_text}

현재 사용자 요청:
{user_input}
"""

                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.9,
                        max_output_tokens=1024,
                    )
                )

                ai_response = response.text

                if not ai_response:
                    ai_response = "죄송해요. 응답을 생성하지 못했어요."

                st.markdown(ai_response)

                # AI 응답 저장
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_response
                })

            except Exception as e:
                error_message = f"""
❌ 오류가 발생했습니다.

에러 내용:
`{str(e)}`

잠시 후 다시 시도해주세요.
"""

                st.error(error_message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "오류가 발생했어요. 잠시 후 다시 시도해주세요."
                })
