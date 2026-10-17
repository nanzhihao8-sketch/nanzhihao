@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Thunder DeepSeek Bot - Dedup Patch

echo ============================================================
echo    Thunder DeepSeek WeChat Bot
echo    De-duplicate message patch
echo ============================================================
echo.

set "VPY=%USERPROFILE%\AppData\Local\wechatbot\venv\Scripts\python.exe"

if exist "%VPY%" (
    echo [OK] Found the bot virtual environment.
    echo.
    "%VPY%" "%~dp0patch-dedup.py"
    goto :done
)

echo [WARN] Virtual environment not found:
echo        %VPY%
echo.
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found on this computer.
    echo         Install Python 3.11+ first, or run install.bat of the bot.
    goto :done
)
echo [INFO] Trying the system Python ...
echo.
python "%~dp0patch-dedup.py"

:done
echo.
echo ============================================================
echo   Finished. Press any key to close this window.
echo ============================================================
pause >nul