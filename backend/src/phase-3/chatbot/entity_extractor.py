"""Entity Extractor for Phase III AI Chatbot

This module extracts relevant entities from natural language input
such as todo titles, due dates, priorities, and statuses.
"""

import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.constants import EntityType, TodoPriority, TodoStatus


class EntityExtractor:
    """Extracts entities from natural language input"""

    def __init__(self):
        # Regex patterns for different entity types
        self.date_patterns = [
            r'tomorrow',
            r'today',
            r'next\s+(week|monday|tuesday|wednesday|thursday|friday|saturday|sunday)',
            r'yesterday',
            r'in\s+(\d+)\s+(days?|weeks?|months?)',
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'(\d{4}-\d{2}-\d{2})',
            r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{1,2})(st|nd|rd|th)?',
        ]

        self.priority_patterns = {
            'high': [r'high', r'urgent', r'asap', r'immediately', r'important'],
            'medium': [r'medium', r'normal', r'regular'],
            'low': [r'low', r'when convenient', r'whenever', r'not urgent'],
        }

        self.status_patterns = {
            'completed': [r'completed', r'done', r'finished', r'closed'],
            'pending': [r'pending', r'not done', r'not finished', r'open'],
        }

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract various entities from the input text

        Args:
            text: Natural language input from user

        Returns:
            Dictionary mapping entity types to extracted values
        """
        entities = {
            'todo_title': self._extract_todo_title(text),
            'due_date': self._extract_due_dates(text),
            'priority': self._extract_priority(text),
            'status': self._extract_status(text),
        }

        # Clean up empty lists
        return {k: v for k, v in entities.items() if v}

    def _extract_todo_title(self, text: str) -> List[str]:
        """
        Extract potential todo titles from the text

        Args:
            text: Input text

        Returns:
            List of potential todo titles
        """
        text_lower = text.lower()

        # Patterns to identify todo titles based on context
        title_patterns = [
            # After "add" or "create" until common endings
            r'(?:add|create|make|new)\s+(.+?)(?:\s+to|\s+in|\s+on|\s+my|\s+the|$|,|\.|and)',
            # After "buy", "get", "do", etc.
            r'(?:buy|get|do|finish|complete|call|send|order|prepare|schedule|attend|watch|read|write)\s+(.+?)(?:\s+by|\s+for|\s+on|\s+at|\s+to|\s+from|\s+before|\s+after|,|\.|$)',
            # After "grocery", "shopping", etc.
            r'(?:grocery|shopping|errand):\s*(.+?)(?:\s+and|\s+also|,|\.|$)',
            # After "update" or "change" - this is what was missing!
            r'(?:update|change|modify|edit)\s+(.+?)\s+(?:to|with)',
            # After "mark" or "set" - IMPROVED PATTERN to avoid capturing the status part
            r'(?:mark|set)\s+(.+?)\s+(?:as|to)\s+(?:complete|done|finished|pending|in progress|high|medium|low|completed)',
            # After "delete" or "remove"
            r'(?:delete|remove|cancel|clear|eliminate|get rid of)\s+(.+?)(?:\s+from|\s+off|\s+on|\s+the|\s+my|\s*$|,|\.|and)',
        ]

        titles = []
        for pattern in title_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                # Handle the case where re.findall returns tuples due to capture groups
                if isinstance(match, tuple):
                    # Take the first non-empty group from the tuple
                    for group in match:
                        if group and group.strip():
                            titles.append(group.strip())
                            break
                elif match and match.strip():
                    titles.append(match.strip())

        # Additional cleanup and refinement
        refined_titles = []
        for title in titles:
            # Remove common stop words at the beginning
            title = re.sub(r'^(the|a|an)\s+', '', title)
            # Remove trailing punctuation
            title = title.rstrip('.,;!')
            if len(title) > 0:
                refined_titles.append(title)

        # Deduplicate while preserving order
        seen = set()
        unique_titles = []
        for title in refined_titles:
            if title.lower() not in seen:
                seen.add(title.lower())
                unique_titles.append(title)

        # Special case: if we're dealing with a "mark as" command, try to extract the original title
        if any(word in text_lower for word in ['mark', 'set']) and any(word in text_lower for word in ['as', 'to']):
            # Look for the original todo title in a more intelligent way
            # If the command is "Mark buy milk as complete", we want "buy milk"
            mark_as_pattern = r'(?:mark|set)\s+(.+?)\s+(?:as|to)\s+(?:complete|done|finished|pending|in progress|high|medium|low|completed)'
            mark_match = re.search(mark_as_pattern, text_lower, re.IGNORECASE)
            if mark_match:
                extracted_title = mark_match.group(1).strip()
                # Remove common stop words at the beginning
                extracted_title = re.sub(r'^(the|a|an)\s+', '', extracted_title)
                extracted_title = extracted_title.rstrip('.,;!')
                if extracted_title and extracted_title not in unique_titles:
                    unique_titles.insert(0, extracted_title)  # Put it first priority

        return unique_titles

    def _extract_due_dates(self, text: str) -> List[str]:
        """
        Extract potential due dates from the text

        Args:
            text: Input text

        Returns:
            List of potential due dates in ISO format
        """
        text_lower = text.lower()
        dates = []

        # Match various date patterns
        for pattern in self.date_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = ' '.join([m for m in match if m])

                # Convert to actual date
                parsed_date = self._parse_date_string(match.strip(), text_lower)
                if parsed_date:
                    dates.append(parsed_date)

        # Deduplicate while preserving order
        seen = set()
        unique_dates = []
        for date in dates:
            if date not in seen:
                seen.add(date)
                unique_dates.append(date)

        return unique_dates

    def _parse_date_string(self, date_str: str, context: str = "") -> Optional[str]:
        """
        Parse a date string and convert to ISO format

        Args:
            date_str: Date string to parse
            context: Full context for additional parsing

        Returns:
            Date in ISO format (YYYY-MM-DD) or None
        """
        date_str = date_str.lower().strip()

        try:
            # Handle relative dates
            if 'tomorrow' in date_str:
                return (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            elif 'today' in date_str:
                return datetime.now().strftime('%Y-%m-%d')
            elif 'yesterday' in date_str:
                return (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            elif 'next week' in date_str:
                return (datetime.now() + timedelta(weeks=1)).strftime('%Y-%m-%d')
            elif 'next monday' in date_str:
                days_ahead = 0 - datetime.now().weekday() + 7  # Next Monday
                return (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
            elif 'next tuesday' in date_str:
                days_ahead = 1 - datetime.now().weekday() + 7  # Next Tuesday
                return (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
            elif 'next wednesday' in date_str:
                days_ahead = 2 - datetime.now().weekday() + 7  # Next Wednesday
                return (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
            elif 'next thursday' in date_str:
                days_ahead = 3 - datetime.now().weekday() + 7  # Next Thursday
                return (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
            elif 'next friday' in date_str:
                days_ahead = 4 - datetime.now().weekday() + 7  # Next Friday
                return (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
            elif 'next saturday' in date_str:
                days_ahead = 5 - datetime.now().weekday() + 7  # Next Saturday
                return (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
            elif 'next sunday' in date_str:
                days_ahead = 6 - datetime.now().weekday() + 7  # Next Sunday
                return (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')

            # Handle "in X days/weeks/months"
            in_pattern = r'in\s+(\d+)\s+(day|week|month)s?'
            in_match = re.search(in_pattern, date_str)
            if in_match:
                num = int(in_match.group(1))
                unit = in_match.group(2)
                if 'day' in unit:
                    return (datetime.now() + timedelta(days=num)).strftime('%Y-%m-%d')
                elif 'week' in unit:
                    return (datetime.now() + timedelta(weeks=num)).strftime('%Y-%m-%d')
                elif 'month' in unit:
                    # Approximate: add 30 days per month
                    return (datetime.now() + timedelta(days=num * 30)).strftime('%Y-%m-%d')

            # Handle MM/DD/YYYY or DD/MM/YYYY or YYYY-MM-DD formats
            date_formats = ['%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d', '%m-%d-%Y', '%d-%m-%Y']
            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(date_str, fmt)
                    return parsed_date.strftime('%Y-%m-%d')
                except ValueError:
                    continue

            # Handle month day formats like "January 15th"
            month_day_pattern = r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{1,2})(st|nd|rd|th)?'
            month_day_match = re.search(month_day_pattern, date_str)
            if month_day_match:
                month_str = month_day_match.group(1).capitalize()
                day = int(month_day_match.group(2))
                month_num = datetime.strptime(month_str, '%B').month
                current_year = datetime.now().year
                parsed_date = datetime(current_year, month_num, day)

                # If the date is in the past, use next year
                if parsed_date < datetime.now():
                    parsed_date = datetime(current_year + 1, month_num, day)

                return parsed_date.strftime('%Y-%m-%d')

        except Exception:
            # If parsing fails, return None
            pass

        return None

    def _extract_priority(self, text: str) -> List[str]:
        """
        Extract priority levels from the text

        Args:
            text: Input text

        Returns:
            List of priority levels
        """
        text_lower = text.lower()
        priorities = []

        for priority, patterns in self.priority_patterns.items():
            for pattern in patterns:
                if re.search(r'\b' + pattern + r'\b', text_lower, re.IGNORECASE):
                    priorities.append(priority.upper())

        # Deduplicate while preserving order
        seen = set()
        unique_priorities = []
        for priority in priorities:
            if priority not in seen:
                seen.add(priority)
                unique_priorities.append(priority)

        return unique_priorities

    def _extract_status(self, text: str) -> List[str]:
        """
        Extract status values from the text

        Args:
            text: Input text

        Returns:
            List of status values
        """
        text_lower = text.lower()
        statuses = []

        for status, patterns in self.status_patterns.items():
            for pattern in patterns:
                if re.search(r'\b' + pattern + r'\b', text_lower, re.IGNORECASE):
                    statuses.append(status.upper())

        # Deduplicate while preserving order
        seen = set()
        unique_statuses = []
        for status in statuses:
            if status not in seen:
                seen.add(status)
                unique_statuses.append(status)

        return unique_statuses


if __name__ == "__main__":
    # Example usage
    extractor = EntityExtractor()

    test_inputs = [
        "Add buy groceries by Friday",
        "Create task to finish report by January 15th",
        "Show my high priority todos",
        "Mark buy groceries as completed",
        "Schedule meeting with John next week",
        "Update learn python to complete",
        "Set test task from user login to done"
    ]

    for inp in test_inputs:
        entities = extractor.extract_entities(inp)
        print(f"Input: {inp}")
        print(f"Entities: {entities}")
        print("---")