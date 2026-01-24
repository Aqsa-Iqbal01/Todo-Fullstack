#!/bin/bash
# Script to start the complete Todo Chatbot system

echo "Starting Todo Chatbot System..."

# Check if required dependencies are installed
if ! command -v python &> /dev/null; then
    echo "Python is not installed. Please install Python 3.8+"
    exit 1
fi

if ! command -v pip &> /dev/null; then
    echo "Pip is not installed. Please install pip"
    exit 1
fi

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Check if backend is already running
if check_port 8004; then
    echo "Warning: Port 8004 (Backend) is already in use!"
    read -p "Do you want to continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Exiting..."
        exit 1
    fi
else
    echo "Port 8004 is available for Backend"
fi

# Check if MCP server is already running
if check_port 8080; then
    echo "Warning: Port 8080 (MCP Server) is already in use!"
    read -p "Do you want to continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Exiting..."
        exit 1
    fi
else
    echo "Port 8080 is available for MCP Server"
fi

# Start the backend server in the background
echo "Starting Backend Server on port 8004..."
python run_backend_with_db_init.py &
BACKEND_PID=$!

# Wait a moment for the backend to start
sleep 3

# Start the MCP server in the background
echo "Starting MCP Server on port 8080..."
cd phase-3 && python -m start_mcp_server &
MCP_PID=$!

# Create a file to track the PIDs for easy cleanup
echo "$BACKEND_PID $MCP_PID" > todo_chatbot_pids.txt

echo
echo "==========================================="
echo "TODO CHATBOT SYSTEM IS NOW RUNNING"
echo "==========================================="
echo "Backend Server: http://localhost:8004"
echo "MCP Server: http://localhost:8080"
echo "PIDs saved to: todo_chatbot_pids.txt"
echo
echo "To test the system:"
echo "1. Register/Login to get an auth token"
echo "2. Test with: curl -X POST http://localhost:8004/api/chatbot \\"
echo "   -H 'Authorization: Bearer YOUR_TOKEN' \\"
echo "   -H 'Content-Type: application/json' \\"
echo "   -d '{\"message\": \"Add buy groceries to my list\"}'"
echo
echo "To stop the system: run stop_system.sh"
echo "==========================================="

# Wait for both processes
wait $BACKEND_PID $MCP_PID