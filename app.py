import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. API 키 설정 (본인의 키를 넣어주세요!)
# ==========================================
# 내 키를 클라우드 금고(Secrets)에서 꺼내 쓰는 방식
# (로컬에서 테스트할 때는 오류가 날 수 있으니, 지금은 수정하고 저장만 하세요)
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# ==========================================
# 2. [핵심] 사용 가능한 모델 자동 찾기
# ==========================================
def get_available_model():
    try:
        # 내 키로 사용할 수 있는 모델 목록을 가져옵니다.
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # 이름에 'flash'나 'pro'가 들어가는 최신 모델을 우선 선택
                if 'flash' in m.name or 'pro' in m.name:
                    return m.name
        # 못 찾으면 기본값 반환
        return "models/gemini-pro"
    except Exception as e:
        return "models/gemini-pro"

# 자동으로 찾은 모델 이름 (예: models/gemini-1.5-flash-001)
active_model_name = get_available_model()

# ==========================================
# 3. AI 모델 설정
# ==========================================
system_prompt = """
당신은 10년 차 IT 서비스 전문 Product Manager입니다. 
클라이언트가 앱 아이디어를 이야기하면, 상세한 PRD를 작성하세요.
반드시 아래 목차를 포함하여 Markdown으로 출력하세요.
1. 프로젝트 개요 (배경, 목적, 타겟)
2. 핵심 기능 명세 (기능명, 설명, 우선순위)
3. 유저 스토리
4. 기술 스택 추천
5. 데이터 모델 초안
"""

model = genai.GenerativeModel(
    model_name=active_model_name, # 여기서 자동으로 찾은 이름을 씁니다
    system_instruction=system_prompt
)

# ==========================================
# 4. 웹사이트 화면 구성
# ==========================================
st.set_page_config(page_title="PRD Generator", layout="wide")

st.title("🚀 AI 앱 기획자 (PRD 생성기)")
st.caption(f"현재 연결된 AI 모델: {active_model_name}") # 연결된 모델 이름을 화면에 표시
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("💡 아이디어 입력")
    user_input = st.text_area("어떤 앱을 만들고 싶으신가요?", height=300)
    generate_btn = st.button("기획서 생성하기 ✨", type="primary")

with col2:
    st.subheader("📄 완성된 기획서")
    if generate_btn and user_input:
        with st.spinner("기획서를 작성 중입니다..."):
            try:
                response = model.generate_content(user_input)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"오류 발생: {e}")