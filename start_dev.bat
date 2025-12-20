@echo off
chcp 65001 >nul
echo ========================================
echo Next.js 개발 서버 시작
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] 의존성 확인 중...
if not exist "node_modules" (
    echo 의존성을 설치합니다...
    call npm install
    echo.
)

echo [2/2] 개발 서버 시작 중...
echo.
echo 브라우저에서 다음 주소로 접속하세요:
echo http://localhost:3000
echo.
echo 서버를 종료하려면 Ctrl+C를 누르세요.
echo.

call npm run dev

pause

