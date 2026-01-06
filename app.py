import streamlit as st
import google.generativeai as genai
import os

# ==========================================
# 1. API 키 설정
# ==========================================
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    # 로컬 테스트용 (배포 시에는 Secrets가 우선됨)
    GOOGLE_API_KEY = "YOUR_TEST_API_KEY"

if not GOOGLE_API_KEY or GOOGLE_API_KEY.startswith("YOUR_TEST"):
    pass 
else:
    genai.configure(api_key=GOOGLE_API_KEY)

# ==========================================
# 2. 모델 설정 (Gemini 2.5 flash 강제 지정)
# ==========================================
# 사용자가 'Pro' 성능을 원하므로 모델을 명시적으로 지정하는 것이 좋습니다.
# 최신 모델인 gemini-2.5-flash를 사용합니다.
MODEL_NAME = "gemini-2.5-flash" 

# ==========================================
# 3. 프롬프트 엔지니어링 (개발 최적화)
# ==========================================
# AI가 '코딩하기 좋은' 답변을 내놓도록 시스템 프롬프트를 완전히 재설계했습니다.
system_prompt = """
당신은 Google의 수석 소프트웨어 아키텍트이자 풀스택 개발자입니다.
사용자의 아이디어를 바탕으로, AI 코딩 도구(Cursor, GitHub Copilot, Google AI Studio)가 
**즉시 실행 가능한 코드를 생성할 수 있도록** 완벽한 '개발 설계서'를 작성해야 합니다.

반드시 다음 형식(Markdown)을 엄격하게 지켜주세요. 서술형 문장보다는 구조화된 명세를 선호합니다.

## 1. 프로젝트 구조 (Project Structure)
- 폴더 및 파일 트리 구조를 ASCII 형태로 보여주세요.
- 각 파일의 역할을 한 줄로 명시하세요.

## 2. 필수 라이브러리 (requirements.txt)
- 프로젝트 실행에 꼭 필요한 패키지명과 버전을 명시하세요.
- 호환성 문제가 없는 안정적인 라이브러리를 선정하세요.

## 3. 핵심 로직 명세 (Core Logic Specs)
- **app.py (메인 파일):** UI 구성 요소, 세션 상태 관리, 이벤트 처리 로직을 의사 코드(Pseudo-code) 혹은 핵심 스니펫으로 작성하세요.
- **데이터 처리:** 외부 API 호출, 데이터 파싱 등의 로직을 구체적으로 설명하세요.
- **에러 핸들링:** API 키 누락, 요청 실패 등 예외 상황에 대한 처리 방침을 명시하세요.

## 4. 개발 가이드 (Step-by-Step Implementation)
1. 환경 설정 방법
2. 코드 작성 순서
3. 실행 명령어

**주의사항:**
- 디자인보다는 '기능 구현'과 '코드의 완결성'에 집중하세요.
- Streamlit을 사용할 경우, 최신 문법(st.query_params 등)을 반영하세요.
"""

# ==========================================
# 4. 화면 구성
# ==========================================
st.set_page_config(page_title="AI 개발 설계자 - Dev Spec 생성기", page_icon="💻", layout="wide")

st.title("💻 AI 개발 설계자 (Dev Spec Generator)")
st.caption(f"Powered by {MODEL_NAME} | 개발자를 위한 상세 구현 명세서 생성")

if not GOOGLE_API_KEY:
    st.error("API 키가 설정되지 않았습니다.")
    st.stop()

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    system_instruction=system_prompt
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("🛠️ 앱 아이디어 입력")
    user_input = st.text_area(
        "구현하고 싶은 기능을 구체적으로 적어주세요.", 
        height=300, 
        placeholder="예: 사용자가 PDF를 업로드하면 내용을 요약해주고, 관련된 퀴즈를 3개 생성해주는 Streamlit 앱을 만들고 싶어."
    )
    generate_btn = st.button("개발 명세서 생성하기 ⚙️", type="primary", use_container_width=True)

with col2:
    st.subheader("📋 개발 구현 명세서")
    if generate_btn and user_input:
        with st.spinner("아키텍처를 설계하고 코드 구조를 잡는 중입니다..."):
            try:
                # 생성 설정: 토큰 수를 넉넉하게 잡아야 코드가 잘리지 않습니다.
                response = model.generate_content(
                    user_input,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7, # 창의성보다는 논리적인 구조 중요
                        max_output_tokens=4000
                    )
                )
                st.markdown(response.text)
            except Exception as e:
                st.error(f"생성 중 오류 발생: {e}")
    elif generate_btn:
        st.warning("아이디어를 입력해주세요!")


