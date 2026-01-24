# Todo Chatbot Intent Classification Reference

## Intent Types

### CREATE_TODO
- **Purpose**: Create a new todo item
- **Common Phrases**:
  - "Add buy groceries to my list"
  - "Create a task to call mom"
  - "Put workout at 6pm on my todo list"
  - "Remind me to finish the report"
  - "Need to schedule dentist appointment"

### READ_TODOS
- **Purpose**: Retrieve and display existing todo items
- **Common Phrases**:
  - "Show my todos"
  - "Display my task list"
  - "What do I have to do today?"
  - "List all my tasks"
  - "Check my to-do list"

### UPDATE_TODO
- **Purpose**: Modify an existing todo item (usually marking as complete/incomplete)
- **Common Phrases**:
  - "Mark buy groceries as complete"
  - "Finish the report task"
  - "Mark workout as done"
  - "Set the meeting as completed"
  - "Unmark the task as incomplete"

### DELETE_TODO
- **Purpose**: Remove a todo item from the list
- **Common Phrases**:
  - "Delete the meeting with John"
  - "Remove buy groceries from my list"
  - "Cancel the workout task"
  - "Erase the reminder to call mom"

### GENERAL_CONVERSATION
- **Purpose**: Handle non-todo related queries
- **Common Topics**:
  - Weather inquiries: "What's the weather like?"
  - Jokes: "Tell me a joke"
  - Entertainment: "What movies are good?"
  - Greetings: "Hello", "How are you?"

### UNKNOWN
- **Purpose**: Catch unrecognized intents
- **Fallback Response**: Guide user to proper todo commands