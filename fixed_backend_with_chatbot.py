import os
import sys
from pathlib import Path

# Add the root directory to Python path first
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Add phase-3 directory and its subdirectories to Python path
phase3_dir = root_dir / "phase-3"
sys.path.insert(0, str(phase3_dir))

# Add all phase-3 subdirectories to Python path
for subdir in ["chatbot", "mcp_server", "mcp_server/tools", "adapters", "services", "config"]:
    subdir_path = phase3_dir / subdir
    if subdir_path.exists():
        sys.path.insert(0, str(subdir_path))

# Now try to import and patch the modules before importing main
def patch_modules():
    """Patch modules to fix import issues"""
    import importlib.util

    # Patch the chatbot module to use absolute imports
    chatbot_path = phase3_dir / "chatbot" / "chat_interface.py"
    if chatbot_path.exists():
        spec = importlib.util.spec_from_file_location("chatbot.chat_interface", chatbot_path)
        chatbot_module = importlib.util.module_from_spec(spec)
        sys.modules['chatbot.chat_interface'] = chatbot_module

    # Patch the mcp server module
    mcp_server_path = phase3_dir / "mcp_server" / "server.py"
    if mcp_server_path.exists():
        spec = importlib.util.spec_from_file_location("mcp_server.server", mcp_server_path)
        mcp_server_module = importlib.util.module_from_spec(spec)
        sys.modules['mcp_server.server'] = mcp_server_module

    # Patch the tools modules
    for tool_file in (phase3_dir / "mcp_server" / "tools").glob("*.py"):
        if tool_file.name != '__init__.py':
            tool_name = tool_file.stem
            spec = importlib.util.spec_from_file_location(f"mcp_server.tools.{tool_name}", tool_file)
            tool_module = importlib.util.module_from_spec(spec)
            sys.modules[f'mcp_server.tools.{tool_name}'] = tool_module

# Apply patches before importing main
patch_modules()

# Now import the main backend app
from backend.src.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)