# ⚛️ Open Claw 기반 원자력 인허가 규제 검증 멀티 에이전트 시스템
> **Kaist OverEdge 공동창업자 지원 프로그램 기술 프로토타입**

본 프로젝트는 방대하고 복잡한 원자력 규제 가이드라인(NUREG-0800 등)과 설계 도면 간의 교차 검증 및 인허가 문서 작성 프로세스를 자율적으로 자동화하는 **RegTech SaaS 멀티 에이전트 파이프라인**의 MVP 프로토타입입니다.

## 🚀 Key Features
- **오픈소스 Open Claw 아키텍처 반영:** 로우 레벨 백엔드 제어가 가능한 Open Claw 프레임워크의 자율 에이전트 통신 및 공유 메모리 메커니즘을 Streamlit 상에 구현.
- **다중 에이전트(Multi-Agent) 협업:** 1. `도면 분석 에이전트 (Vision-to-Data)`
  2. `규제 검증 에이전트 (RAG & Reasoning)`
  3. `보고서 서기 에이전트 (Structured Generation)`
- **자율 피드백 루프 (Self-Correction Loop):** 단방향 파이프라인을 넘어, 에이전트 간 상호 교차 검증 및 역방향 피드백을 통해 결과물의 품질을 스스로 고도화하는 엔드투엔드 오케스트레이션 실현.

## 📦 설치 및 실행 방법 (Local)
```bash
git clone [https://github.com/berrylee019/nuclear-regulatory-agents.git]
cd nuclear-regulatory-agents
pip install -r requirements.txt
streamlit run app.py
