# 식물성 케톤식 영양강좌 수요조사 - Next.js 버전

Vercel 배포용 Next.js 프로젝트입니다.

## 🚀 빠른 시작

### 로컬 개발

```bash
npm install
npm run dev
```

브라우저에서 http://localhost:3000 접속

### Vercel 배포

1. GitHub에 푸시
2. https://vercel.com 접속
3. GitHub 저장소 연결
4. 자동 배포 완료!

## 📝 주요 기능

- ✅ 설문지 표시 및 응답 수집
- ✅ 주관식 질문 지원
- ✅ 관리자 로그인
- ✅ 반응형 디자인 (모바일/데스크톱)

## ⚠️ 주의사항

### 데이터 저장
Vercel은 서버리스 환경이므로 파일 저장이 제한적입니다.

**현재 상태:**
- 설문 제출은 성공하지만 실제 저장은 구현되지 않음

**해결 방법:**
1. **Vercel KV** 사용 (Key-Value 저장소)
2. **Supabase** 또는 **MongoDB** 등 데이터베이스 연동
3. **Vercel Blob Storage** 사용

### 다음 단계
데이터베이스 연동을 통해 완전한 기능 구현 필요

## 📁 프로젝트 구조

```
ask2/
├── pages/
│   ├── index.tsx          # 메인 설문 페이지
│   ├── admin.tsx          # 관리자 로그인
│   ├── statistics.tsx     # 통계 페이지
│   ├── submit-success.tsx # 제출 성공 페이지
│   └── api/
│       ├── submit.ts      # 설문 제출 API
│       └── admin/
│           └── login.ts   # 로그인 API
├── public/
│   └── survey.json        # 설문지 데이터
└── package.json
```

## 🔐 관리자 계정

- 아이디: `admin`
- 비밀번호: `1234`
