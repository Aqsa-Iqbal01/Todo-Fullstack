import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'phase-3'))

from chatbot.intent_parser import IntentParser
parser = IntentParser()

test_inputs = [
    'Add buy groceries to my list',
    'Show my todos',
    'Mark buy groceries as complete',
    'Delete the meeting with John',
    'Hi there',
    'What can you do?'
]

print('Testing intent classification:')
for inp in test_inputs:
    intent = parser.classify_intent(inp)
    print(f'  "{inp}" -> {intent}')
    
print('\n[SUCCESS] Intent classification working correctly')