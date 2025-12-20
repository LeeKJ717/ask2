# Vercel 배포 문제 해결 가이드

## 현재 상태 확인

### 1. Vercel 대시보드 확인
- https://vercel.com/dashboard 접속
- `ask2` 프로젝트 선택
- "Deployments" 탭에서 최신 배포 확인

### 2. 빌드 로그 확인
- 배포를 클릭하여 상세 정보 확인
- "Build Logs"에서 오류 메시지 확인

## 일반적인 문제와 해결 방법

### 문제 1: TypeScript 오류
**증상**: 빌드 실패, TypeScript 타입 오류

**해결**:
```bash
# 로컬에서 빌드 테스트
cd ask2
npm install
npm run build
```

### 문제 2: 의존성 문제
**증상**: 패키지 설치 실패

**해결**: `package.json` 확인 및 수정

### 문제 3: 파일 경로 문제
**증상**: survey.json을 찾을 수 없음

**해결**: `public/survey.json` 파일 위치 확인

## 빠른 해결 방법

### 방법 1: Vercel에서 재배포
1. Vercel 대시보드에서 프로젝트 선택
2. "Deployments" → 최신 배포의 "..." 메뉴
3. "Redeploy" 클릭

### 방법 2: GitHub에서 재배포 트리거
```bash
cd ask2
git commit --allow-empty -m "Trigger redeploy"
git push
```

### 방법 3: 로컬 빌드 테스트
```bash
cd ask2
npm install
npm run build
```

빌드가 성공하면 Vercel에서도 성공할 가능성이 높습니다.

## 오류 메시지가 있다면
Vercel 대시보드의 빌드 로그에서 오류 메시지를 복사하여 알려주세요.

