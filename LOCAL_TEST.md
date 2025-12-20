# 로컬에서 테스트하는 방법

## 1단계: Node.js 설치

1. https://nodejs.org/ 접속
2. LTS 버전 다운로드 및 설치
3. 설치 완료 후 컴퓨터 재시작 (필요시)

## 2단계: 의존성 설치

```bash
cd C:\Users\UserK\Desktop\ask2
npm install
```

## 3단계: 개발 서버 실행

```bash
npm run dev
```

## 4단계: 브라우저에서 접속

- 자동으로 브라우저가 열리거나
- 수동으로 http://localhost:3000 접속

## 5단계: 테스트

- 설문지가 정상적으로 표시되는지 확인
- 모든 기능이 작동하는지 테스트
- 문제가 없으면 GitHub에 푸시

## 문제 해결

### npm이 인식되지 않는 경우
- Node.js 설치 후 PowerShell 재시작
- 또는 명령 프롬프트(cmd) 사용

### 포트 3000이 사용 중인 경우
- 다른 터미널에서 실행 중인 서버 종료
- 또는 다른 포트 사용: `npm run dev -- -p 3001`

