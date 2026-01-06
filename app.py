import streamlit as st
import google.generativeai as genai
import os

# ==========================================
# 1. API 키 설정 (클라우드 & 로컬 호환)
# ==========================================
try:
    # 1순위: Streamlit Cloud의 비밀 금고(Secrets)에서 키를 가져옴
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    # 2순위: 로컬(내 컴퓨터) 환경변수나 직접 입력 (테스트용)
    # 배포 시에는 Secrets가 작동하므로 이 부분은 무시됩니다.
    GOOGLE_API_KEY = "여기에_테스트용_API_키를_넣어도_됩니다" 

# API 키가 없으면 경고 메시지 띄우기
if not GOOGLE_API_KEY or GOOGLE_API_KEY == "여기에_테스트용_API_키를_넣어도_됩니다":
    # 키가 설정되지 않았을 때의 안전장치
    pass 
else:
    genai.configure(api_key=GOOGLE_API_KEY)

# ==========================================
# 2. 모델 자동 감지 (오류 방지용)
# ==========================================
def get_available_model():
    try:
        if not GOOGLE_API_KEY: return "models/gemini-pro"
        
        # 사용 가능한 모델 목록 조회
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'flash' in m.name or 'pro' in m.name:
                    return m.name
        return "models/gemini-pro"
    except Exception:
        return "models/gemini-pro"

# ==========================================
# 3. 웹사이트 화면 구성
# ==========================================
st.set_page_config(page_title="AI 기획자 - PRD 생성기", page_icon="📝", layout="wide")

st.title("🚀 AI 앱 기획자 (PRD 생성기)")

# API 키가 정상인지 확인
if not GOOGLE_API_KEY or GOOGLE_API_KEY.startswith("여기에"):
    st.error("🚨 API 키가 설정되지 않았습니다!")
    st.info("Streamlit Cloud의 [Settings] > [Secrets] 메뉴에 GOOGLE_API_KEY를 등록해주세요.")
    st.stop() # 여기서 실행 중단

# 모델 설정
active_model = get_available_model()
st.caption(f"연결된 AI 모델: {active_model}")
st.markdown("---")

# 프롬프트 설정
system_prompt = """
당신은 10년 차 IT 서비스 전문 Product Manager입니다. 
클라이언트가 앱 아이디어를 이야기하면, 개발팀이 바로 작업할 수 있는 상세한 PRD를 작성하세요.
반드시 아래 형식을 지켜 Markdown으로 출력하세요.

1. 프로젝트 개요 (배경, 목적, 타겟)
2. 핵심 기능 명세 (기능명, 설명, 우선순위 P0/P1)
3. 유저 스토리 (Who, What, Why)
4. 기술 스택 추천 (App, Server, DB)
5. 데이터 모델 초안
"""

model = genai.GenerativeModel(
    model_name=active_model,
    system_instruction=system_prompt
)

# 화면 레이아웃
col1, col2 = st.columns(2)

with col1:
    st.subheader("💡 아이디어 입력")
    user_input = st.text_area("어떤 앱을 만들고 싶으신가요?", height=300, placeholder="예: 2030 직장인을 위한 취미 공유 플랫폼...")
    generate_btn = st.button("기획서 생성하기 ✨", type="primary", use_container_width=True)

with col2:
    st.subheader("📄 완성된 기획서")
    if generate_btn:
        if not user_input:
            st.warning("아이디어를 입력해주세요!")
        else:
            with st.spinner("AI PM이 기획서를 작성 중입니다..."):
                try:
                    response = model.generate_content(user_input)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
