'use client';

import { useState, useRef, useEffect } from 'react';
import { useSession } from '@/contexts/SessionContext';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

const ChatbotInterface = () => {
  const [messages, setMessages] = useState<Message[]>([
    { id: '1', text: 'Hello! I\'m your AI assistant. How can I help you manage your todos today?', sender: 'bot', timestamp: new Date() }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Get token from SessionContext
  const { token } = useSession();

  // Track if user has scrolled away from bottom
  const [isAtBottom, setIsAtBottom] = useState(true);

  // Check if user is at bottom of chat
  const checkIsAtBottom = () => {
    const container = document.getElementById('messages-container');
    if (container) {
      const isNearBottom = container.scrollHeight - container.scrollTop - container.clientHeight < 10;
      setIsAtBottom(isNearBottom);
      return isNearBottom;
    }
    return true;
  };

  // Handle scroll events to track user position
  useEffect(() => {
    const container = document.getElementById('messages-container');
    if (container) {
      const handleScroll = () => {
        checkIsAtBottom();
      };

      container.addEventListener('scroll', handleScroll);
      return () => container.removeEventListener('scroll', handleScroll);
    }
  }, []);

  // Scroll to bottom of messages when new messages arrive, but only if user is already at bottom
  useEffect(() => {
    if (isAtBottom) {
      scrollToBottom();
    }
  }, [messages, isAtBottom]);

  // Always scroll to bottom when loading state changes (thinking/typing)
  useEffect(() => {
    scrollToBottom();
  }, [isLoading]);

  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      // Scroll to the bottom of the container
      const container = document.getElementById('messages-container');
      if (container) {
        container.scrollTop = container.scrollHeight;
        setIsAtBottom(true);
      }
    }
  };

  
  const handleSendMessage = async () => {
    if (!inputText.trim() || isLoading) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      // Get token from multiple sources as fallback
      let authToken = token;

      // If token is not available from SessionContext, try localStorage
      if (!authToken) {
        authToken = localStorage.getItem('token');
      }

      // If still no token, try to get from sessionStorage
      if (!authToken) {
        authToken = sessionStorage.getItem('token');
      }

      // Check if token exists before making the request
      if (!authToken) {
        throw new Error('No authentication token found. Please log in first.');
      }

      // Ensure the token is properly formatted (remove any extra whitespace or prefixes)
      let cleanAuthToken = authToken.trim();
      if (cleanAuthToken.startsWith('Bearer ')) {
        cleanAuthToken = cleanAuthToken.substring(7).trim();
      } else if (cleanAuthToken.toLowerCase().startsWith('bearer ')) {
        cleanAuthToken = cleanAuthToken.substring(6).trim();
      }

      // Log the token being used for debugging (remove in production)
      console.log('Sending request to chatbot with token (length):', cleanAuthToken.length);

      // Call the chatbot API route (which will eventually connect to the backend)
      const response = await fetch('/api/chatbot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${cleanAuthToken}`
        },
        body: JSON.stringify({
          message: inputText
        })
      });

      console.log('Chatbot API response status:', response.status);

      const data = await response.json();

      let botResponse: Message;

      if (data.success) {
        // Extract operation type to determine if we need to refresh the dashboard
        const operationResult = data.response?.operation_result;
        const intentProcessed = data.response?.intent_processed;

        // Extract todos from various possible response locations
        let todosFromResponse = null;
        if (data.response?.operation_result?.todos) {
          todosFromResponse = data.response?.operation_result?.todos;
        } else if (Array.isArray(data.response?.operation_result) && data.response?.operation_result.length > 0) {
          // Check if operation_result itself is an array of todos
          todosFromResponse = data.response?.operation_result;
        } else if (data.response?.operation_result && typeof data.response?.operation_result === 'object' && 'data' in data.response?.operation_result) {
          // Check if operation_result has a 'data' property containing todos
          todosFromResponse = data.response?.operation_result?.data;
        } else {
          // Fallback: check if operation_result itself contains todo properties
          todosFromResponse = null;
        }

        // Create bot response
        let responseText = data.response?.message || data.message || 'I processed your request successfully!';

        // If this is a READ_TODOS operation and we have todos, show them in a structured way
        if (intentProcessed === 'READ_TODOS' && Array.isArray(todosFromResponse) && todosFromResponse.length > 0) {
          // Add structured todo list to the response
          const todoListText = '\n\n📋 Your Todo List:\n' +
                              todosFromResponse.map((todo: any, index: number) =>
                                `${index + 1}. ${todo.title || todo.name || 'Untitled'}${todo.completed || todo.status === 'COMPLETED' ? ' ✅' : ' ❌'}`
                              ).join('\n');
          responseText += todoListText;
        }

        botResponse = {
          id: Date.now().toString(),
          text: responseText,
          sender: 'bot',
          timestamp: new Date()
        };

        // Trigger dashboard refresh if this operation affects the todo list
        // We'll refresh for any successful operation that modifies the todo list
        if (intentProcessed &&
            (intentProcessed === 'CREATE_TODO' ||
             intentProcessed === 'UPDATE_TODO' ||
             intentProcessed === 'DELETE_TODO' ||
             intentProcessed.includes('CREATE_TODO') ||
             intentProcessed.includes('UPDATE_TODO') ||
             intentProcessed.includes('DELETE_TODO'))) {
          // Save timestamp of the update to localStorage
          localStorage.setItem('lastTodoUpdate', new Date().toISOString());

          // Dispatch a custom event to notify the dashboard to refresh
          window.dispatchEvent(new CustomEvent('todosUpdated', { detail: { operation: intentProcessed } }));
        } else if (intentProcessed === 'READ_TODOS') {
          // Even for read operations, we should update the timestamp so the dashboard knows it's up to date
          localStorage.setItem('lastTodoUpdate', new Date().toISOString());
        }
      } else {
        // Handle different possible error structures
        let errorMessage = 'Sorry, I encountered an error processing your request.';

        if (data.error && typeof data.error === 'object') {
          if (data.error.message) {
            errorMessage = data.error.message;
          } else if (data.error.detail) {
            errorMessage = data.error.detail;
          }
        } else if (data.error_message) {
          errorMessage = data.error_message;
        } else if (data.message) {
          errorMessage = data.message;
        } else if (typeof data === 'string') {
          errorMessage = data;
        }

        botResponse = {
          id: Date.now().toString(),
          text: errorMessage,
          sender: 'bot',
          timestamp: new Date()
        };
      }

      setMessages(prev => [...prev, botResponse]);
    } catch (error) {
      const errorMessage: Message = {
        id: Date.now().toString(),
        text: 'Sorry, I\'m having trouble connecting to the AI service. Please try again.',
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-[600px] max-w-3xl mx-auto border-0 rounded-2xl shadow-xl bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-800 dark:to-gray-900 overflow-hidden">
      {/* Chat Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-6">
        <div className="flex items-center space-x-3">
          <div className="bg-white/20 p-2 rounded-full">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <div>
            <h2 className="text-xl font-bold">AI Todo Assistant</h2>
            <p className="text-sm opacity-90">Manage your tasks with natural language</p>
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-6 bg-white/50 dark:bg-gray-800/30 relative max-h-[350px]" id="messages-container">
        <div className="space-y-4 pb-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[85%] px-5 py-3 rounded-2xl rounded-tr-none ${
                  message.sender === 'user'
                    ? 'bg-gradient-to-r from-blue-500 to-indigo-500 text-white rounded-br-none'
                    : 'bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200 shadow-sm rounded-tl-none border border-gray-200 dark:border-gray-600'
                }`}
              >
                <p className="whitespace-pre-wrap break-words">{message.text}</p>
                <p className={`text-xs mt-2 ${message.sender === 'user' ? 'text-blue-100' : 'text-gray-500 dark:text-gray-400'}`}>
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </p>
              </div>
            </div>
          ))}
        </div>
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white dark:bg-gray-700 max-w-[85%] px-5 py-3 rounded-2xl rounded-tl-none shadow-sm border border-gray-200 dark:border-gray-600">
              <div className="flex items-center space-x-2">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce delay-75"></div>
                  <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce delay-150"></div>
                </div>
                <span className="text-sm text-gray-600 dark:text-gray-300">Thinking...</span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-gray-800">
        <div className="flex gap-3">
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your todo command (e.g., 'Add buy Groceries to my list')..."
            className="flex-1 border border-gray-300 dark:border-gray-600 rounded-2xl px-4 py-3 resize-none h-20 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 transition-all duration-200"
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={isLoading || !inputText.trim()}
            className={`self-end px-6 py-3 rounded-2xl text-white font-medium shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-0.5 ${
              isLoading || !inputText.trim()
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700'
            }`}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        </div>
        <div className="mt-3 text-sm text-gray-600 dark:text-gray-400 bg-blue-50 dark:bg-gray-700/50 rounded-lg p-3">
          <span className="font-medium text-indigo-700 dark:text-indigo-300">Tips:</span> Try commands like "Add finish report by Friday", "Show my todos", "Mark buy Groceries as complete", "Remove task", or "Update task to new description"
        </div>
      </div>
    </div>
  );
};

export default ChatbotInterface;



