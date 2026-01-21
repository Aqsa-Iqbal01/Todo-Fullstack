"""Conversation Service for Phase III AI Chatbot

This module manages conversation context between related user requests.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from ..config.settings import settings


class ConversationContext:
    """Represents the context of a conversation"""

    def __init__(self, conversation_id: str = None):
        self.conversation_id = conversation_id or str(uuid.uuid4())
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.messages = []
        self.user_context = {}
        self.pending_actions = []
        self.context_data = {}

    def add_message(self, role: str, content: str):
        """Add a message to the conversation"""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now()
        })
        self.last_activity = datetime.now()

    def update_user_context(self, **kwargs):
        """Update user-specific context data"""
        self.user_context.update(kwargs)

    def set_pending_action(self, action: str, data: Dict[str, Any]):
        """Set a pending action for follow-up"""
        self.pending_actions.append({
            "action": action,
            "data": data,
            "timestamp": datetime.now()
        })

    def clear_pending_actions(self):
        """Clear all pending actions"""
        self.pending_actions.clear()

    def update_context_data(self, key: str, value: Any):
        """Update specific context data"""
        self.context_data[key] = value

    def is_expired(self) -> bool:
        """Check if the conversation context has expired"""
        expiry_time = self.last_activity + timedelta(hours=1)  # 1 hour expiry
        return datetime.now() > expiry_time


class ConversationService:
    """Service for managing conversation contexts"""

    def __init__(self):
        self.conversations: Dict[str, ConversationContext] = {}
        self.max_conversations = 1000  # Maximum number of concurrent conversations

    def get_or_create_conversation(self, conversation_id: Optional[str] = None) -> ConversationContext:
        """
        Get an existing conversation or create a new one

        Args:
            conversation_id: Optional conversation ID

        Returns:
            Conversation context object
        """
        if conversation_id and conversation_id in self.conversations:
            context = self.conversations[conversation_id]
            if context.is_expired():
                del self.conversations[conversation_id]
                context = ConversationContext(conversation_id)
                self.conversations[conversation_id] = context
        else:
            context = ConversationContext(conversation_id)
            self.conversations[context.conversation_id] = context

        # Clean up expired conversations periodically
        self._cleanup_expired()

        return context

    def get_conversation(self, conversation_id: str) -> Optional[ConversationContext]:
        """
        Get a specific conversation by ID

        Args:
            conversation_id: Conversation ID

        Returns:
            Conversation context object or None if not found/expired
        """
        if conversation_id not in self.conversations:
            return None

        context = self.conversations[conversation_id]
        if context.is_expired():
            del self.conversations[conversation_id]
            return None

        return context

    def update_conversation(self, conversation_id: str, **kwargs) -> bool:
        """
        Update a conversation with new information

        Args:
            conversation_id: Conversation ID
            **kwargs: Data to update

        Returns:
            True if successful, False otherwise
        """
        context = self.get_conversation(conversation_id)
        if not context:
            return False

        for key, value in kwargs.items():
            if hasattr(context, key):
                setattr(context, key, value)
            else:
                context.update_context_data(key, value)

        return True

    def add_message_to_conversation(self, conversation_id: str, role: str, content: str) -> bool:
        """
        Add a message to a conversation

        Args:
            conversation_id: Conversation ID
            role: Role of the message sender ('user' or 'bot')
            content: Content of the message

        Returns:
            True if successful, False otherwise
        """
        context = self.get_conversation(conversation_id)
        if not context:
            return False

        context.add_message(role, content)
        return True

    def clear_conversation(self, conversation_id: str) -> bool:
        """
        Clear a conversation's context

        Args:
            conversation_id: Conversation ID

        Returns:
            True if successful, False otherwise
        """
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            return True
        return False

    def _cleanup_expired(self):
        """Clean up expired conversations to prevent memory leaks"""
        expired_ids = []
        for conv_id, context in self.conversations.items():
            if context.is_expired():
                expired_ids.append(conv_id)

        for conv_id in expired_ids:
            del self.conversations[conv_id]

        # Also limit the total number of conversations
        if len(self.conversations) > self.max_conversations:
            # Remove oldest conversations
            sorted_convs = sorted(self.conversations.items(),
                                key=lambda x: x[1].last_activity)
            to_remove = len(self.conversations) - self.max_conversations
            for i in range(to_remove):
                if i < len(sorted_convs):
                    del self.conversations[sorted_convs[i][0]]


# Global conversation service instance
conversation_service = ConversationService()