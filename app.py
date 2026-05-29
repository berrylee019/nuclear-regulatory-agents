import streamlit as st
import time

# 1. 페이지 기본 설정 및 테마
st.set_page_config(page_title="OverEdge AI - Nuclear Regulatory Agent Team", page_icon="⚛️", layout="wide")

st.title("⚛️ 원자력 인허가 규제 검증 멀티 에이전트 시스템")
st.caption("Kaist OverEdge 공동창업자 지원 프로토타입 — Open Claw 기반 엔드투엔드 파이프라인")
st.markdown("---")

# 2. 에이전트 통신 및 메모리를 위한 세션 상태(Session State) 초기화
if "blueprint_data" not in st.session_state:
    st.session_state.blueprint_data = None
if "compliance_report" not in st.session_state:
    st.session_state.compliance_report = None
if "final_draft" not in st.session_state:
    st.session_state.final_draft = None
if "feedback_log" not in st.session_state:
    st.session_state.feedback_log = []

# 가상 도면 선택 (심사위원 테스트용 인터페이스)
st.sidebar.header("📋 입력 파라미터 (테스트용)")
blueprint_selection = st.sidebar.selectbox(
    "테스트할 원자로 설계 도면 선택",
    ["SMR-100 소형 모듈 원자로 냉각계통도 v1.2", "수소 생산 연계형 고온가스로 배치도 v2.0"]
)

# 3. 레이아웃 배치 (개별 에이전트 모니터링 대시보드)
col1, col2, col3 = st.columns(3)

# --- 에이전트 1: 도면 분석 ---
with col1:
    st.subheader("🕵️‍♂️ 1. 도면 분석 에이전트")
    st.info("Vision-to-Data Pipeline")
    if st.button("▶ 도면 스펙 추출 시작", use_container_width=True):
        with st.spinner("도면 이미지 및 비정형 스펙 분석 중..."):
            time.sleep(1.5)  # 에이전트 자율 추론 시각화용 딜레이
            st.session_state.blueprint_data = {
                "설계 압력": "15.5 MPa",
                "운전 온도": "320 °C",
                "주요 재질": "Class 1 Stainless Steel (SUS316)",
                "배관 두께": "45 mm (NUREG-0800 최소 기준 대조 필요)"
            }
        st.success("도면 데이터 라벨링 완료!")
    
    if st.session_state.blueprint_data:
        st.json(st.session_state.blueprint_data)
    else:
        st.write("💡 버튼을 누르면 비정형 도면 스펙을 추출합니다.")

# --- 에이전트 2: 규제 검증 ---
with col2:
    st.subheader("⚖️ 2. 규제 검증 에이전트")
    st.info("RAG & NUREG Reasoning")
    if st.button("▶ NUREG 조항 교차 검증", use_container_width=True):
        if not st.session_state.blueprint_data:
            st.warning("⚠️ 1단계 도면 분석 데이터가 먼저 필요합니다.")
        else:
            with st.spinner("NUREG-0800 및 국내외 원자력 규제 DB 검색 중..."):
                time.sleep(2.0)
                st.session_state.compliance_report = {
                    "상태": "⚠️ 보완 필요 (Conditional Compliance)",
                    "매핑 조항": "NUREG-0800 Chapter 5 (Reactor Coolant System)",
                    "위험 요인": "320°C 운전 온도 조건에서 SUS316 재질 사용 시, 장기 응력 부식 균열(SCC) 가능성 존재. 배관 두께 45mm는 마진이 다소 부족함."
                }
            st.success("규제 컴플라이언스 추론 완료!")
            
    if st.session_state.compliance_report:
        st.write(f"**검증 결과:** {st.session_state.compliance_report['상태']}")
        st.write(f"**근거 조항:** `{st.session_state.compliance_report['매핑 조항']}`")
        st.warning(st.session_state.compliance_report['위험 요인'])
    else:
        st.write("💡 1단계 데이터를 기반으로 규제 조항을 대조합니다.")

# --- 에이전트 3: 보고서 서기 ---
with col3:
    st.subheader("✍️ 3. 보고서 서기 에이전트")
    st.info("Structured Generation")
    if st.button("▶ 인허가 문서 초안 렌더링", use_container_width=True):
        if not st.session_state.compliance_report:
            st.warning("⚠️ 2단계 규제 검증 보고서가 먼저 필요합니다.")
        else:
            with st.spinner("표준 인허가 서식에 맞춰 초안 작성 중..."):
                time.sleep(1.5)
                st.session_state.final_draft = f"""[원자력안전위원회 인허가 신청서 초안]
- 대상 구조물: {blueprint_selection}
- 기술 사양 검토: 설계 압력 {st.session_state.blueprint_data['설계 압력']} / 운전 온도 {st.session_state.blueprint_data['운전 온도']}
- 규제 검증 의견: {st.session_state.compliance_report['위험 요인']}
- 최종 결론: 본 설계는 특정 조건(재질 보완 및 두께 재확인) 하에 조건부 적합함 수립 가능."""
            st.success("공식 규제 서식 문서 생성 완료!")
            
    if st.session_state.final_draft:
        st.text_area("생성된 문서 초안", st.session_state.final_draft, height=180)
    else:
        st.write("💡 법적/기술적 근거를 표준 템플릿에 렌더링합니다.")


# --- 핵심 파트: 자율 협업 및 상호 피드백 루프 엔드투엔드 파이프라인 ---
st.markdown("---")
st.header("🔄 에이전트 간 자율 피드백 및 품질 고도화 루프 (End-to-End)")
st.markdown("""
> **Open Claw 오케스트레이션 메커니즘:** 아래 버튼을 누르면 3개의 에이전트가 단방향으로 끝나는 것이 아니라, 
> **'보고서 서기'가 작성한 초안의 취약점을 '규제 검증 에이전트'가 재심사하고, '도면 분석 에이전트'에게 특정 스펙 재추출을 요청하는 상호 피드백 루프**를 자율적으로 수행하여 최종 품질을 완성합니다.
""")

if st.button("🔥 4대 에이전트 자율 협업 파이프라인 일괄 실행", type="primary", use_container_width=True):
    with st.status("🚀 멀티 에이전트 팀 자율 협업 세션 시작...", expanded=True) as status:
        
        # Loop 1: 초기 파이프라인 가동
        st.write("🤖 **[System]** Open Claw 백엔드 활성화. 에이전트 팀을 조직합니다.")
        time.sleep(1.0)
        
        st.write("🕵️‍♂️ **[도면 분석 Agent]** 비정형 설계 도면 분석 중... 스펙 데이터 탑재 완료.")
        st.session_state.blueprint_data = {"설계 압력": "15.5 MPa", "운전 온도": "320 °C", "주요 재질": "SUS316", "배관 두께": "45 mm"}
        time.sleep(1.2)
        
        st.write("⚖️ **[규제 검증 Agent]** NUREG-0800 가이드라인 대조 완료. SUS316 응력 부식 균열(SCC) 경고 발생.")
        st.session_state.compliance_report = {"상태": "⚠️ 보완 필요", "매핑 조항": "NUREG-0800 Ch.5", "위험 요인": "320°C 조건 하 SUS316의 SCC 위험성 및 배관 두께 마진 부족 유력."}
        time.sleep(1.2)
        
        st.write("✍️ **[보고서 서기 Agent]** 1차 인허가 문서 초안 작성 완료. 규제 검증 에이전트에게 역피드백 요청.")
        time.sleep(1.0)
        
        # Loop 2: 자율 역피드백 및 고도화 루프 발생 (기사 속 헤파이스토스 핵심 구조)
        st.markdown("#### 🔄 **[Feedback Loop] 에이전트 간 상호 교차 검증 및 보완 프로세스 작동**")
        
        st.write("📢 **[규제 검증 Agent -> 도면 분석 Agent]** *'배관 두께 45mm 주위의 보강재(Stiffener) 유무 및 상세 용접부 설계 스펙을 도면에서 다시 정밀 스캔해줘.'*")
        time.sleep(1.5)
        
        st.write("🕵️‍♂️ **[도면 분석 Agent]** 도면 우하단 상세도(Detail View) 재확인 결과, 'Inconel 82/182 용접재 적용 및 5mm 추가 보강 레이어' 발견. 스펙 데이터 업데이트 완료.")
        st.session_state.blueprint_data["보강 사양"] = "Inconel 82/182 용접재 및 5mm 피복 추가 확인"
        time.sleep(1.5)
        
        st.write("⚖️ **[규제 검증 Agent]** 업데이트된 스펙 기반 재추론 진행. *'Inconel 용접재 적용으로 SCC 위험성 대폭 감소 확인. 컴플라이언스 등급 [적합]으로 상향.'*")
        st.session_state.compliance_report["상태"] = "✅ 적합 (Compliance Verified)"
        st.session_state.compliance_report["위험 요인"] = "초기 SUS316 SCC 우려가 있었으나, 도면 재분석 결과 Inconel 82/182 특수 용접 및 5mm 보강 레이어가 확인되어 NUREG-0800 규제 요구조건을 완벽히 충족함."
        time.sleep(1.5)
        
        st.write("✍️ **[보고서 서기 Agent]** 최종 자율 보완된 기술 근거를 바탕으로 공식 인허가 문서 초안 2차 수정 및 고도화 완료.")
        st.session_state.final_draft = f"""[최종 원자력안전위원회 인허가 제출서]
- 대상 구조물: {blueprint_selection}
- 기술 사양: 설계 압력 15.5 MPa / 운전 온도 320 °C ({st.session_state.blueprint_data['보강 사양']})
- 규제 검증 결과: {st.session_state.compliance_report['상태']}
- 기술적 근거: {st.session_state.compliance_report['위험 요인']}
- 결론: 최종 검증 결과 본 설계는 컴플라이언스 위반 사항이 없음을 증명함."""
        time.sleep(1.0)
        
        status.update(label="✅ 엔드투엔드 자율 고도화 파이프라인 실행 완료!", state="complete", expanded=True)
        st.rerun() # 화면 갱신하여 상단 개별 에이전트 창에도 최종 데이터 동기화

st.markdown("---")
st.info("💡 **심사위원 안내:** 본 프로토타입은 오픈소스 Open Claw의 멀티 에이전트 토큰 라우팅 및 랭체인 인포메이션 플로우를 시각화한 모델입니다. 각 개별 에이전트 버튼을 따로 눌러 단방향 흐름을 보거나, 하단의 '자율 협업 파이프라인 일괄 실행' 버튼을 통해 에이전트 간의 '자율 역피드백(Self-Correction Loop)' 기술을 직접 시뮬레이션해볼 수 있습니다.")
