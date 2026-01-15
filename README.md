📌 프로젝트명

산업현장 실시간 모니터링 및 위험 감지 시스템

📖 프로젝트 개요

본 프로젝트는 산업 현장에서 발생할 수 있는 위험 요소를
센서 데이터, 실시간 영상, AI 분석을 통해 감지하고
이를 웹 대시보드로 시각화하는 시스템이다.

AI는 위험 요소를 분석하여 결과만 전달하며,
백엔드는 해당 정보를 안전하게 저장하고 프론트엔드에 제공한다.

🎯 주요 기능

실시간 센서 데이터 수집 및 저장

AI 기반 위험 요소 감지 및 알림

위험 발생 스냅샷 기록 (DB 저장)

실시간 영상 스트리밍

관리자 대시보드 (React)

🛠 기술 스택
Frontend

React

JavaScript

Chart / Dashboard UI

Backend

Node.js

Supabase (PostgreSQL)

REST API

AI

Python

TensorFlow

YOLO

PyTorch

Database

PostgreSQL (Supabase)

🧱 시스템 아키텍처
[ Sensors ] ─┐
             ├──> [ Node.js Backend ] ──> [ Supabase (Postgres) ]
[ AI Server ]┘            │
                           └──> [ React Frontend ]

[ Camera ] ──> [ Streaming Server ] ──> [ React ]

👥 팀 구성 및 역할
역할	담당
Frontend	React UI / Dashboard
Backend A	DB 설계 / Supabase 관리
Backend B	API / AI 연동 / 영상
AI	모델 개발 및 위험 분석

📌 AI 담당자는 DB 및 프론트에 직접 접근하지 않음

📂 프로젝트 구조
capstone-monitoring/
├── frontend/
├── backend/
├── ai/
├── supabase/
│   └── migrations/
├── docs/
└── README.md

🔐 보안 및 권한 관리

Supabase RLS 적용

Service Role Key는 백엔드에서만 사용

프론트엔드는 anon key만 사용

🚀 실행 방법 (예시)
Frontend
cd frontend
npm install
npm start

Backend
cd backend
npm install
npm run dev

📅 개발 일정

1주차: 기획 및 설계

2주차: DB 및 API 구축

3주차: AI 연동

4주차: 통합 및 테스트

📎 참고 자료

Supabase Docs

React Docs

TensorFlow / PyTorch

✅ 여기까지 하면?

프로젝트 신뢰도 +10

교수님 질문 50% 차단

팀원들 방향 통일