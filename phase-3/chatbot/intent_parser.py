"""Intent Parser for Phase III AI Chatbot

This module handles natural language intent classification
using rule-based and simple ML approaches.
"""

import re
from typing import Dict, List, Tuple
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.constants import IntentType


class IntentParser:
    """Classifies user intent from natural language input"""

    def __init__(self):
        self.patterns = {
            IntentType.CREATE_TODO: [
                r'\b(add|create|make|new|put|set)\b.*\b(todo|task|item|thing|grocery|shopping|list)\b',
                r'\b(add|create|make|new|put|set)\b.*\b(grocery|shopping|errand|appointment|meeting|report|project|idea)\b',
                r'\b(create|add)\b.*\b(to|in|on)\b.*\b(list|todo|task)\b',
                r'\b(need to|want to|have to|must|should)\b.*\b(add|create|make|buy|get|do|finish|complete|write|call|send|order)\b',
            ],
            IntentType.READ_TODOS: [
                r'\b(show|list|display|see|view|what|check|look|tell me|give me)\b.*\b(my|current|existing|pending|active)\b.*\b(todo|task|item|list|things)\b',
                r'\b(what|show|list|display|view|see)\b.*\b(have to|got to|need to|to do|todo|tasks)\b',
                r'\b(do i|did i|what)\b.*\b(have|got|placed|put)\b.*\b(on|in)\b.*\b(my|the)\b.*\b(list|todo|task)\b',
                r'\b(all|my|current|existing|pending|active)\b.*\b(todo|task|item|list|things)\b',
            ],
            IntentType.UPDATE_TODO: [
                r'\b(mark|set|change|update|modify|edit|complete|finish|done)\b.*\b(as|to|be)\b.*\b(complete|done|finished|completed|pending|in progress|high|medium|low)\b',
                r'\b(update|change|modify|edit)\b.*\b(title|name|description|due date|priority)\b',
                r'\b(mark|set|make)\b.*\b(done|completed|finished|complete)\b',
                r'\b(unmark|uncomplete|reopen|reset)\b.*\b(done|completed|finished|complete)\b',
            ],
            IntentType.DELETE_TODO: [
                r'\b(delete|remove|cancel|clear|eliminate|get rid of|scratch|drop)\b.*\b(todo|task|item|thing|from|off)\b.*\b(list|my|the)\b',
                r'\b(remove|delete|cancel)\b.*\b(from|off)\b.*\b(my|the)\b.*\b(list|todo|task)\b',
                r'\b(no need|don\'t need|don\'t want|cancel|forget)\b.*\b(that|it|the)\b',
            ],
            # Add patterns for general conversation
            IntentType.GENERAL_CONVERSATION: [
                r'\b(hi|hello|hey|greetings|good morning|good afternoon|good evening|good day|morning|afternoon|evening|day)\b',
                r'\b(what|how|who|where|when|why|can|could|would|will|should)\b.*\b(you|assistant|bot|help|manage|todo|task|list)\b',
                r'\b(help|support|assist|aid|guide|direct|advise|suggest)\b',
                r'\b(what can|what do|what does|what is|what are|how do|how can|how to)\b.*\b(you|this|these|those|it|app|application|system)\b',
            ]
        }

        # Simple keywords for fallback classification
        self.keyword_map = {
            IntentType.CREATE_TODO: ['add', 'create', 'new', 'make', 'put', 'set'],
            IntentType.READ_TODOS: ['show', 'list', 'display', 'see', 'view', 'what', 'check'],
            IntentType.UPDATE_TODO: ['mark', 'set', 'change', 'update', 'modify', 'edit', 'complete', 'done', 'finish'],
            IntentType.DELETE_TODO: ['delete', 'remove', 'cancel', 'clear', 'eliminate'],
            # Add keywords for general conversation
            IntentType.GENERAL_CONVERSATION: ['hi', 'hello', 'hey', 'greetings', 'help', 'what', 'how', 'can', 'please']
        }

    def classify_intent(self, text: str) -> str:
        """
        Classify the intent of the given text

        Args:
            text: Natural language input from user

        Returns:
            Classified intent as a string
        """
        text_lower = text.lower().strip()

        # First, try pattern matching
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return intent.value

        # Fallback to keyword matching
        scores = {}
        for intent, keywords in self.keyword_map.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[intent.value] = score

        # Return the intent with highest score, or UNKNOWN if no matches
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        else:
            return IntentType.UNKNOWN.value

    def get_confidence_score(self, text: str) -> Dict[str, float]:
        """
        Get confidence scores for all intents

        Args:
            text: Natural language input from user

        Returns:
            Dictionary mapping intents to confidence scores
        """
        text_lower = text.lower().strip()
        scores = {intent.value: 0.0 for intent in IntentType}

        # Score based on pattern matches
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    scores[intent.value] += 0.5  # High confidence for pattern match

        # Score based on keyword matches
        for intent, keywords in self.keyword_map.items():
            keyword_count = sum(1 for keyword in keywords if keyword in text_lower)
            scores[intent.value] += keyword_count * 0.1  # Lower confidence for keyword match

        # Normalize scores to 0-1 range
        max_score = max(scores.values()) if scores.values() else 1
        if max_score > 0:
            for intent in scores:
                scores[intent] /= max_score

        return scores


if __name__ == "__main__":
    # Example usage
    parser = IntentParser()

    test_inputs = [
        "Add buy groceries to my list",
        "Show my todos",
        "Mark buy groceries as complete",
        "Delete the meeting with John",
        "Update the due date of finish report to Friday",
        "Hi",
        "Hello",
        "What can you do?",
        "How can you help me?",
        "Help me with my todos"
    ]

    for inp in test_inputs:
        intent = parser.classify_intent(inp)
        confidence_scores = parser.get_confidence_score(inp)
        print(f"Input: {inp}")
        print(f"Intent: {intent}")
        print(f"Confidence scores: {confidence_scores}")
        print("---")