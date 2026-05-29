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

# --- [자율형 오케스트레이션 전용 세션 메모리 풀 추가] ---
if "auto_logs" not in st.session_state:
    st.session_state.auto_logs = []
if "blackboard" not in st.session_state:
    st.session_state.blackboard = {
        "current_step": "IDLE",
        "blueprint_specs": {},
        "compliance_verdict": {},
        "document_draft": "",
        "loop_count": 0,
        "quality_approved": False
    }

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


# ==================================================================================
# 🔥 [NEW] 하단 추가: '헤파이스토스'형 자율 오케스트레이션 완전 무인 자동화 파트
# ==================================================================================
st.markdown("---")
st.header("🧠 Open Claw 커스텀: 무인 자율 오케스트레이션 엔진 (Autonomous Engine)")
st.markdown("""
> **인간 개입 제로(0) 자율 최적화:** 아래 버튼을 누르면, 시스템이 중앙 공유 메모리(Blackboard)를 구성하고 
> 목표 규제 점수(95점)에 도달할 때까지 **에이전트들이 스스로 피드백 토큰을 주고받으며 무한 루프 검증**을 수행합니다. 
> 임프레시브한 실시간 릴레이 라우팅 로그가 동적으로 출력됩니다.
""")

# 자율형 전용 레이아웃 분할
auto_col_left, auto_col_right = st.columns([3, 2])

with auto_col_left:
    st.subheader("📡 자율 통신 라이브 라우팅 (Live Agent Relay Logs)")
    log_placeholder = st.empty()
    
    # 자율형 로그 출력 스트리밍 함수
    def print_auto_log(agent, icon, msg, status_type="info"):
        entry = {"time": time.strftime("%H:%M:%S"), "agent": agent, "icon": icon, "msg": msg, "type": status_type}
        st.session_state.auto_logs.append(entry)
        with log_placeholder.container():
            for log in st.session_state.auto_logs[-6:]: # 최근 6개 로그 집중 노출
                if log["type"] == "success":
                    st.success(f"[{log['time']}] {log['icon']} **{log['agent']}**: {log['msg']}")
                elif log["type"] == "warning":
                    st.warning(f"[{log['time']}] {log['icon']} **{log['agent']}**: {log['msg']}")
                elif log["type"] == "error":
                    st.error(f"[{log['time']}] {log['icon']} **{log['agent']}**: {log['msg']}")
                else:
                    st.info(f"[{log['time']}] {log['icon']} **{log['agent']}**: {log['msg']}")

with auto_col_right:
    st.subheader("💾 실시간 전역 공유 메모리 (Blackboard Pool)")
    state_placeholder = st.empty()
    state_placeholder.json(st.session_state.blackboard)

# 자율 실행 구동 버튼
if st.button("🚀 무인 자율 오케스트레이션 엔진 시동", type="secondary", use_container_width=True):
    # 전용 상태 초기화
    st.session_state.auto_logs = []
    st.session_state.blackboard = {
        "current_step": "INITIALIZING", "blueprint_specs": {}, "compliance_verdict": {}, "document_draft": "", "loop_count": 0, "quality_approved": False
    }
    
    print_auto_log("Orchestrator Router", "🧠", "Open Claw 자율형 인프라가 켜졌습니다. 통신 인터페이스를 마운트합니다.")
    time.sleep(1.0)
    
    # 퀄리티 스코어가 합격점에 도달할 때까지 무한 컨테이너 자율 제어
    while not st.session_state.blackboard["quality_approved"]:
        st.session_state.blackboard["loop_count"] += 1
        loop = st.session_state.blackboard["loop_count"]
        
        print_auto_log("Orchestrator Router", "🧠", f"🔄 [CYCLE #{loop}] 에이전트 간 토큰 분배 및 컴플라이언스 루프 시작.")
        time.sleep(0.8)
        
        # [에이전트 1 단계]
        st.session_state.blackboard["current_step"] = f"LOOP_{loop}_STEP_1_BLUEPRINT"
        state_placeholder.json(st.session_state.blackboard)
        
        if loop == 1:
            print_auto_log("도면 분석 Agent", "🕵️‍♂️", f"'{blueprint_selection}' 비정형 설계도 분석 수행. 기본 물리량 매핑 시작.")
            time.sleep(1.5)
            st.session_state.blackboard["blueprint_specs"] = {"설계 압력": "15.5 MPa", "운전 온도": "320 °C", "재질": "SUS316", "두께": "45 mm"}
            print_auto_log("도면 분석 Agent", "🕵️‍♂️", "1차 원자료 사양 추출 완료 -> 공유 메모리 적재.", "success")
        else:
            print_auto_log("도면 분석 Agent", "🕵️‍♂️", "📢 [역피드백 접수] NUREG-0800 장기 응력 균열 차단을 위한 용접 패스 및 피복 두께 정밀 재스캔 착수.")
            time.sleep(2.0)
            st.session_state.blackboard["blueprint_specs"]["보강재"] = "Inconel 82/182 용접재 및 5mm 특수 내열 피복층 발견"
            print_auto_log("도면 분석 Agent", "🕵️‍♂️", "보완 스펙 검출 완료 -> 공유 메모리 동기화 완료.", "success")
            
        state_placeholder.json(st.session_state.blackboard)
        time.sleep(1.0)
        
        # [에이전트 2 단계]
        st.session_state.blackboard["current_step"] = f"LOOP_{loop}_STEP_2_COMPLIANCE"
        state_placeholder.json(st.session_state.blackboard)
        print_auto_log("규제 검증 Agent", "⚖️", "공유 메모리 변화 감지. 최신 NUREG 규제 조항 DB RAG 대조 추론 엔진 가동.")
        time.sleep(1.5)
        
        if loop == 1:
            st.session_state.blackboard["compliance_verdict"] = {"품질점수": "72점 / 100점", "상태": "❌ 인허가 거부 위험", "이유": "320°C 고온부 SUS316 단독 적용 시 응력 내부 부식 균열(SCC) 잠재 결함 유력."}
            print_auto_log("규제 검증 Agent", "⚖️", "품질 기준(95점) 미달! 도면 분석 에이전트 측에 서브 스펙 재요청 생성.", "error")
        else:
            st.session_state.blackboard["compliance_verdict"] = {"품질점수": "98점 / 100점", "상태": "✅ 인허가 완벽 적합", "이유": "추가 보강된 Inconel 합금 용접재 매핑으로 고온 SCC 위험 제거 입증."}
            print_auto_log("규제 검증 Agent", "⚖️", "컴플라이언스 최종 패스. 목표 점수 도달.", "success")
            
        state_placeholder.json(st.session_state.blackboard)
        time.sleep(1.0)
        
        # [에이전트 3 단계]
        st.session_state.blackboard["current_step"] = f"LOOP_{loop}_STEP_3_WRITER"
        state_placeholder.json(st.session_state.blackboard)
        print_auto_log("보고서 서기 Agent", "✍️", "법적 검증 결과 풀(Pool)을 기반으로 원자력안전위원회 표준 서식 렌더링.")
        time.sleep(1.2)
        
        if loop == 1:
            st.session_state.blackboard["document_draft"] = f" [1차 불합격 초안] 구조물: {blueprint_selection} / 결과: 보완 명령 하달 예정."
            print_auto_log("보고서 서기 Agent", "✍️", "불완전 인허가 서식 빌드됨. 라우터에 오케스트레이션 사이클 재시작 요청.", "warning")
        else:
            st.session_state.blackboard["document_draft"] = f" [최종 인허가 합격 통과서] 구조물: {blueprint_selection} / 최종 결과: 컴플라이언스 검증 완료 수립."
            print_auto_log("보고서 서기 Agent", "✍️", "NUREG 규제 완벽 대응 인허가 보고서 패키징 완료.", "success")
            st.session_state.blackboard["quality_approved"] = True
            
        state_placeholder.json(st.session_state.blackboard)
        time.sleep(1.2)
        
    st.session_state.blackboard["current_step"] = "AUTONOMOUS_COMPLETE"
    state_placeholder.json(st.session_state.blackboard)
    print_auto_log("Orchestrator Router", "🧠", "🎉 [자율 최적화 완결] 인간의 개입 없이 툴이 스스로 문서를 완전체로 빌드해냈습니다.", "success")
    
    # 상단 기존 대시보드 상태와 동기화
    st.session_state.blueprint_data = st.session_state.blackboard["blueprint_specs"]
    st.session_state.compliance_report = {"상태": "✅ 자율 최적화 완료", "매핑 조항": "NUREG-0800 Ch.5", "위험 요인": "에이전트 팀 자율 피드백을 통해 보강재 스펙 추적 및 인허가 적합성 증명 완결."}
    st.session_state.final_draft = st.session_state.blackboard["document_draft"]
    st.toast("자율 오케스트레이션 엔진 완료! 상단 대시보드가 실시간 동기화되었습니다.", icon="🧠")

st.markdown("---")
st.info("💡 **심사위원 안내:** 본 프로토타입은 오픈소스 Open Claw의 멀티 에이전트 토큰 라우팅 및 랭체인 인포메이션 플로우를 시각화한 모델입니다. 각 개별 에이전트 버튼을 따로 눌러 단방향 흐름을 보거나, 하단의 '자율 협업 파이프라인 일괄 실행' 버튼을 통해 에이전트 간의 '자율 역피드백(Self-Correction Loop)' 기술을 직접 시뮬레이션해볼 수 있습니다.")
