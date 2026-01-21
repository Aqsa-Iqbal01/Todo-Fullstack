"""Enhanced Intent Parser using OpenAI for Phase III AI Chatbot

This module handles natural language intent classification using OpenAI API
for more sophisticated understanding of user input.
"""

import openai
import os
from typing import Dict, List, Optional
import sys
import json
from enum import Enum

# Add the phase-3 directory to the path to allow absolute imports
current_dir = os.path.dirname(__file__)
phase3_dir = os.path.dirname(os.path.dirname(current_dir))
if phase3_dir not in sys.path:
    sys.path.insert(0, phase3_dir)

from config.constants import IntentType


class OpenAIIntentParser:
    """Classifies user intent from natural language input using OpenAI"""

    def __init__(self):
        # Initialize OpenAI API key from environment variable
        openai.api_key = os.getenv("OPENAI_API_KEY")

        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set. Please configure it in your .env file.")

    def classify_intent(self, text: str) -> str:
        """
        Classify the intent of the given text using OpenAI

        Args:
            text: Natural language input from user

        Returns:
            Classified intent as a string
        """
        try:
            # Define the possible intents
            intents = {
                "CREATE_TODO": "Add a new todo to your list (e.g., 'Add buy groceries to my list')",
                "READ_TODOS": "View your existing todos (e.g., 'Show my todos' or 'What do I have to do?')",
                "UPDATE_TODO": "Update an existing todo (e.g., 'Mark buy groceries as complete')",
                "DELETE_TODO": "Remove a todo from your list (e.g., 'Delete the meeting with John')",
                "UNKNOWN": "Unable to determine the intent from the input"
            }

            # Create a prompt for OpenAI
            prompt = f"""
            Analyze the following user input and determine the intent.
            Respond with only the intent type from the following options:
            {', '.join(intents.keys())}

            User input: "{text}"

            Intent:
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an intent classifier for a todo management system. Return only the intent type from the specified options. Do not include any other text or explanation."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # Low temperature for consistent results
                max_tokens=20
            )

            # Extract the intent from the response
            intent = response.choices[0].message.content.strip()

            # Validate the intent is one of our expected types
            if intent in intents:
                return intent
            else:
                return IntentType.UNKNOWN.value

        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            # Fallback to rule-based parsing if OpenAI fails
            from .intent_parser import IntentParser
            fallback_parser = IntentParser()
            return fallback_parser.classify_intent(text)

    def extract_entities_openai(self, text: str) -> Dict[str, List[str]]:
        """
        Extract entities from the text using OpenAI

        Args:
            text: Natural language input from user

        Returns:
            Dictionary mapping entity types to extracted values
        """
        try:
            prompt = f"""
            Extract the following entities from the user input:
            - todo_title: The main task or activity
            - due_date: Any date or time mentioned
            - priority: Any priority indicators (high, medium, low)
            - status: Any status indicators (completed, pending, etc.)

            Return the result as a JSON object with arrays for each entity type.
            If an entity is not found, return an empty array for that entity.

            User input: "{text}"

            JSON response:
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an entity extractor for a todo management system. Return only a valid JSON object with the specified entity types as keys and arrays as values. Do not include any other text or explanation."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=200
            )

            # Parse the JSON response
            content = response.choices[0].message.content.strip()

            # Remove any markdown formatting if present
            if content.startswith("```"):
                content = content.split("\n", 1)[1].rsplit("```", 1)[0].strip()

            entities = json.loads(content)

            # Clean up empty arrays
            return {k: v for k, v in entities.items() if v}

        except Exception as e:
            print(f"Error calling OpenAI API for entity extraction: {e}")
            # Fallback to rule-based extraction if OpenAI fails
            from .entity_extractor import EntityExtractor
            fallback_extractor = EntityExtractor()
            return fallback_extractor.extract_entities(text)


# Example usage
if __name__ == "__main__":
    # Example usage
    parser = OpenAIIntentParser()

    test_inputs = [
        "Add buy groceries to my list",
        "Show my todos",
        "Mark buy groceries as complete",
        "Delete the meeting with John",
        "Update the due date of finish report to Friday"
    ]

    for inp in test_inputs:
        intent = parser.classify_intent(inp)
        entities = parser.extract_entities_openai(inp)
        print(f"Input: {inp}")
        print(f"Intent: {intent}")
        print(f"Entities: {entities}")
        print("---")