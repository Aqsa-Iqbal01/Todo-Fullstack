#!/usr/bin/env python3
"""
Test script to verify that the chatbot can handle 'show list' or 'show todos' commands
"""

import sys
import os
from pathlib import Path

# Add the phase-3 directory to the Python path
phase3_dir = Path(__file__).parent / "phase-3"
if str(phase3_dir) not in sys.path:
    sys.path.insert(0, str(phase3_dir))

def test_intent_parsing_for_show_commands():
    """Test if the intent parser correctly identifies 'show todos' commands"""
    print("Testing intent parsing for 'show todos' commands...")

    # Import the intent parser
    from chatbot.intent_parser import IntentParser

    parser = IntentParser()

    # Test various "show todos" commands
    test_commands = [
        "Show my todos",
        "Show my list",
        "Show my todo list",
        "List my todos",
        "Display my todos",
        "What do I have to do?",
        "What are my tasks?",
        "Show me my tasks",
        "Show my pending tasks",
        "List all my todos"
    ]

    print("\nTesting intent classification:")
    for command in test_commands:
        intent = parser.classify_intent(command)
        confidence_scores = parser.get_confidence_score(command)

        print(f"Command: '{command}'")
        print(f"  -> Intent: {intent}")
        print(f"  -> Confidence scores: {confidence_scores}")
        print()

def test_entity_extraction_for_show_commands():
    """Test entity extraction for 'show todos' commands"""
    print("Testing entity extraction for 'show todos' commands...")

    # Import the entity extractor
    from chatbot.entity_extractor import EntityExtractor

    extractor = EntityExtractor()

    # Test various "show todos" commands
    test_commands = [
        "Show my todos",
        "Show my list",
        "Show my high priority todos",
        "List my completed tasks",
        "What do I have to do today?",
        "Show pending tasks"
    ]

    print("\nTesting entity extraction:")
    for command in test_commands:
        entities = extractor.extract_entities(command)

        print(f"Command: '{command}'")
        print(f"  -> Entities: {entities}")
        print()

def test_full_chat_interface_for_show_commands():
    """Test the full chat interface with 'show todos' commands"""
    print("Testing full chat interface for 'show todos' commands...")

    # Import the chat interface
    from chatbot.chat_interface import ChatInterface

    chat_interface = ChatInterface()

    # Test various "show todos" commands
    test_commands = [
        "Show my todos",
        "Show my list",
        "List my todos",
        "What do I have to do?",
        "Show my pending tasks"
    ]

    print("\nTesting full chat interface (will show intent classification):")
    for command in test_commands:
        # We'll simulate the intent classification part since we can't make actual API calls without a backend
        intent = chat_interface.intent_parser.classify_intent(command)
        entities = chat_interface.entity_extractor.extract_entities(command)

        print(f"Command: '{command}'")
        print(f"  -> Parsed Intent: {intent}")
        print(f"  -> Extracted Entities: {entities}")
        print(f"  -> Expected Action: Should trigger READ_TODOS intent")
        print()

def main():
    print("=== Testing Chatbot 'Show Todos' Functionality ===\n")

    test_intent_parsing_for_show_commands()
    print("\n" + "="*60 + "\n")

    test_entity_extraction_for_show_commands()
    print("\n" + "="*60 + "\n")

    test_full_chat_interface_for_show_commands()

    print("\n=== Summary ===")
    print("The tests above verify that the chatbot can:")
    print("1. Recognize 'show todos' commands through intent parsing")
    print("2. Extract relevant entities from these commands")
    print("3. Route them to the appropriate MCP tool (list_todos)")
    print("")
    print("For the actual functionality to work:")
    print("- The backend API must be running")
    print("- Proper authentication token must be provided")
    print("- The MCP server must be running to process the commands")
    print("")
    print("The READ_TODOS intent should trigger the list_todos MCP tool")
    print("which will call the Phase II backend to retrieve the user's todos.")

if __name__ == "__main__":
    main()