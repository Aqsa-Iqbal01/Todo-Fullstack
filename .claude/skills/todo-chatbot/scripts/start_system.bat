@echo off
REM Batch script to start the complete Todo Chatbot system

echo Starting Todo Chatbot System...

REM Check if required dependencies are installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.8+
    pause
    exit /b 1
)

echo Checking ports...

REM Use netstat to check if ports are in use
netstat -an | find "8004" >nul
if not errorlevel 1 (
    echo Warning: Port 8004 (Backend) is already in use!
    set /p reply=Do you want to continue anyway? (y/N):
    if /i not "%reply%"=="y" (
        echo Exiting...
        pause
        exit /b 1
    )
) else (
    echo Port 8004 is available for Backend
)

netstat -an | find "8080" >nul
if not errorlevel 1 (
    echo Warning: Port 8080 (MCP Server) is already in use!
    set /p reply=Do you want to continue anyway? (y/N):
    if /i not "%reply%"=="y" (
        echo Exiting...
        pause
        exit /b 1
    )
) else (
    echo Port 8080 is available for MCP Server
)

echo Starting Backend Server on port 8004...
start "Backend Server" cmd /c "python run_backend_with_db_init.py"

REM Wait a moment for the backend to start
timeout /t 3 /nobreak >nul

echo Starting MCP Server on port 8080...
start "MCP Server" cmd /c "cd phase-3 && python -m start_mcp_server"

echo.
echo ===========================================
echo TODO CHATBOT SYSTEM IS NOW RUNNING
echo ===========================================
echo Backend Server: http://localhost:8004
echo MCP Server: http://localhost:8080
echo.
echo To test the system:
echo 1. Register/Login to get an auth token
echo 2. Test with: curl -X POST http://localhost:8004/api/chatbot^
echo    -H "Authorization: Bearer YOUR_TOKEN"^
echo    -H "Content-Type: application/json"^
echo    -d "{\"message\": \"Add buy groceries to my list\"}"
echo ===========================================

pause