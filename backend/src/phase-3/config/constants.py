"""Constants definitions for Phase III AI Chatbot"""

from enum import Enum


class IntentType(str, Enum):
    """Types of intents that the chatbot can recognize"""
    CREATE_TODO = "CREATE_TODO"
    READ_TODOS = "READ_TODOS"
    UPDATE_TODO = "UPDATE_TODO"
    DELETE_TODO = "DELETE_TODO"
 
    GENERAL_CONVERSATION = "GENERAL_CONVERSATION"
    UNKNOWN = "UNKNOWN"


class EntityType(str, Enum):
    """Types of entities that can be extracted from user input"""
    TODO_TITLE = "TODO_TITLE"
    DUE_DATE = "DUE_DATE"
    PRIORITY = "PRIORITY"
    STATUS = "STATUS"


class TodoStatus(str, Enum):
    """Possible statuses for todos"""
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN_PROGRESS"


class TodoPriority(str, Enum):
    """Priority levels for todos"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


# Regular expressions for pattern matching
DATE_PATTERNS = [
    r"tomorrow",
    r"today",
    r"next\s+(week|monday|tuesday|wednesday|thursday|friday|saturday|sunday)",
    r"\d{1,2}/\d{1,2}/\d{4}",
    r"\d{4}-\d{2}-\d{2}"
]

# Common synonyms and variations
CREATE_SYNONYMS = ["add", "create", "make", "new", "put", "set"]
READ_SYNONYMS = ["show", "list", "display", "see", "view", "what"]
UPDATE_SYNONYMS = ["update", "change", "modify", "edit", "alter"]
DELETE_SYNONYMS = ["delete", "remove", "cancel", "clear", "eliminate"]
COMPLETE_SYNONYMS = ["complete", "done", "finished", "finish", "mark done"]

# Configuration constants
MIN_CONFIDENCE_SCORE = 0.6
MAX_TODO_TITLE_LENGTH = 200
MAX_ENTITY_EXTRACTION_ATTEMPTS = 3