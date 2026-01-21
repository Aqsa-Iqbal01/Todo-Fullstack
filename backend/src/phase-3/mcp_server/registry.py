"""Tool Registry for MCP Server

This module manages the registration and retrieval of MCP tools.
"""

from typing import Dict, Callable, Any
import asyncio


class ToolRegistry:
    """Registry for managing MCP tools"""

    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._descriptions: Dict[str, str] = {}

    def register_tool(self, name: str, func: Callable, description: str = ""):
        """Register a new tool in the registry"""
        self._tools[name] = func
        if description:
            self._descriptions[name] = description

    def get_tool(self, name: str) -> Callable:
        """Retrieve a tool by name"""
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not found in registry")
        return self._tools[name]

    def get_tool_description(self, name: str) -> str:
        """Get description for a tool"""
        return self._descriptions.get(name, "")

    def list_tools(self) -> Dict[str, str]:
        """List all registered tools with their descriptions"""
        tools_list = {}
        for name in self._tools:
            tools_list[name] = self._descriptions.get(name, "No description available")
        return tools_list

    async def execute_tool(self, name: str, **kwargs) -> Any:
        """Execute a tool asynchronously with given parameters"""
        tool = self.get_tool(name)

        # Check if the tool is async or sync
        if asyncio.iscoroutinefunction(tool):
            return await tool(**kwargs)
        else:
            return tool(**kwargs)


# Global tool registry instance
tool_registry = ToolRegistry()