"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import TodoList from '@/components/TodoList';
import TodoModal from '@/components/TodoModal';
import Navbar from '@/components/Navbar';
import { todoAPI } from '@/lib/api';

interface Todo {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  due_date: string | null;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export default function DashboardPage() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [currentTodo, setCurrentTodo] = useState<Todo | null>(null);
  const [userName, setUserName] = useState<string | null>(null);
  const router = useRouter();

  // Check if user is authenticated and get user info
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }

    // Extract user info from token
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );
      const tokenData = JSON.parse(jsonPayload);
      const email = tokenData.sub || null;

      // Extract name from email (before @ symbol) or use email as fallback
      if (email) {
        const name = email.split('@')[0];
        setUserName(name);
      }
    } catch (error) {
      console.error('Error decoding token:', error);
      // Fallback: try to get user info from localStorage if stored there
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        try {
          const user = JSON.parse(storedUser);
          const name = user.email ? user.email.split('@')[0] : 'User';
          setUserName(name);
        } catch (parseError) {
          console.error('Error parsing stored user:', parseError);
          setUserName('User');
        }
      } else {
        setUserName('User');
      }
    }
  }, [router]);

  // Load todos
  useEffect(() => {
    const fetchTodos = async () => {
      try {
        const response = await todoAPI.getTodos();
        if (response.ok) {
          const data = await response.json();
          setTodos(data);
        } else {
          console.error('Failed to fetch todos');
          // If unauthorized, redirect to login
          if (response.status === 401) {
            localStorage.removeItem('token');
            router.push('/login');
          }
        }
      } catch (error) {
        console.error('Error fetching todos:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTodos();
  }, [router]);

  const handleCreateTodo = () => {
    setCurrentTodo(null);
    setShowModal(true);
  };

  const handleEditTodo = (todo: Todo) => {
    setCurrentTodo(todo);
    setShowModal(true);
  };

  const handleDeleteTodo = async (id: string) => {
    try {
      const response = await todoAPI.deleteTodo(id);
      if (response.ok) {
        setTodos(todos.filter(todo => todo.id !== id));
      } else {
        console.error('Failed to delete todo');
        // If unauthorized, redirect to login
        if (response.status === 401) {
          localStorage.removeItem('token');
          router.push('/login');
        }
      }
    } catch (error) {
      console.error('Error deleting todo:', error);
    }
  };

  const handleToggleTodo = async (id: string) => {
    try {
      const response = await todoAPI.toggleTodo(id);
      if (response.ok) {
        const updatedTodo = await response.json();
        setTodos(todos.map(todo =>
          todo.id === id ? updatedTodo : todo
        ));
      } else {
        console.error('Failed to toggle todo');
        // If unauthorized, redirect to login
        if (response.status === 401) {
          localStorage.removeItem('token');
          router.push('/login');
        }
      }
    } catch (error) {
      console.error('Error toggling todo:', error);
    }
  };

  const handleSaveTodo = async (todoData: Partial<Todo>) => {
    try {
      if (currentTodo) {
        // Update existing todo
        const response = await todoAPI.updateTodo(currentTodo.id, todoData);
        if (response.ok) {
          const updatedTodo = await response.json();
          setTodos(todos.map(todo =>
            todo.id === currentTodo.id ? updatedTodo : todo
          ));
        } else {
          console.error('Failed to update todo');
          // If unauthorized, redirect to login
          if (response.status === 401) {
            localStorage.removeItem('token');
            router.push('/login');
          }
        }
      } else {
        // Create new todo
        const response = await todoAPI.createTodo(todoData);
        if (response.ok) {
          const newTodo = await response.json();
          setTodos([...todos, newTodo]);
        } else {
          console.error('Failed to create todo');
          // If unauthorized, redirect to login
          if (response.status === 401) {
            localStorage.removeItem('token');
            router.push('/login');
          }
        }
      }
    } catch (error) {
      console.error('Error saving todo:', error);
    }
    setShowModal(false);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <Navbar />
        <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
          <div className="text-center py-16">
            <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-r from-indigo-100 to-purple-100 mb-6">
              <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-indigo-600"></div>
            </div>
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Loading your dashboard</h2>
            <p className="text-gray-600 max-w-md mx-auto">
              Preparing your personalized task management experience...
            </p>
            <div className="mt-8 max-w-md mx-auto">
              <div className="bg-white/80 backdrop-blur-sm rounded-xl p-4 border border-gray-200/50 shadow-sm mb-3">
                <div className="animate-pulse flex space-x-4">
                  <div className="flex-1 space-y-3">
                    <div className="h-4 bg-gray-300 rounded w-3/4"></div>
                    <div className="h-4 bg-gray-300 rounded"></div>
                    <div className="h-4 bg-gray-300 rounded w-2/3"></div>
                  </div>
                </div>
              </div>
              <div className="bg-white/80 backdrop-blur-sm rounded-xl p-4 border border-gray-200/50 shadow-sm">
                <div className="animate-pulse flex space-x-4">
                  <div className="flex-1 space-y-3">
                    <div className="h-4 bg-gray-300 rounded w-3/4"></div>
                    <div className="h-4 bg-gray-300 rounded"></div>
                    <div className="h-4 bg-gray-300 rounded w-2/3"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Calculate statistics
  const totalTasks = todos.length;
  const completedTasks = todos.filter(todo => todo.completed).length;
  const pendingTasks = totalTasks - completedTasks;
  const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  // Add custom styles for animations
  const style = `
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }

    @keyframes slideUp {
      from {
        opacity: 0;
        transform: translateY(20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    @keyframes slideIn {
      from {
        opacity: 0;
        transform: translateX(-10px);
      }
      to {
        opacity: 1;
        transform: translateX(0);
      }
    }

    @keyframes fadeInScale {
      from {
        opacity: 0;
        transform: scale(0.95);
      }
      to {
        opacity: 1;
        transform: scale(1);
      }
    }

    @keyframes reveal {
      from {
        opacity: 0;
        transform: scaleY(0);
      }
      to {
        opacity: 1;
        transform: scaleY(1);
      }
    }

    @keyframes progressGrow {
      from { width: 0; }
      to { width: ${completionRate}%; }
    }

    @keyframes bounceOnce {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-10px); }
    }

    .animate-fade-in {
      animation: fadeIn 0.6s ease-out forwards;
    }

    .animate-slide-up {
      animation: slideUp 0.6s ease-out forwards;
    }

    .animate-slide-in {
      animation: slideIn 0.6s ease-out forwards;
    }

    .animate-fade-in-scale {
      animation: fadeInScale 0.4s ease-out forwards;
    }

    .animate-reveal {
      animation: reveal 0.5s ease-out forwards;
    }

    .animate-progress-grow {
      animation: progressGrow 1s ease-out forwards;
    }

    .animate-bounce-once {
      animation: bounceOnce 0.6s ease-in-out;
    }

    .delay-100 { animation-delay: 0.1s; }
    .delay-200 { animation-delay: 0.2s; }
    .delay-300 { animation-delay: 0.3s; }
    .delay-400 { animation-delay: 0.4s; }
    .delay-500 { animation-delay: 0.5s; }
    .delay-700 { animation-delay: 0.7s; }

    .animate-fade-in {
      animation: fadeIn 0.6s ease-out forwards;
    }
  `;

  return (
    <>
      <style>{style}</style>
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <Navbar />
      <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        {/* Header - with fade-in animation */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between mb-8 space-y-6 lg:space-y-0 animate-fade-in">
          <div className="flex-1">
            <h1 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent animate-slide-up">
              Your Todo Dashboard
            </h1>
            {userName && (
              <p className="mt-2 text-gray-600 dark:text-white text-lg animate-slide-up delay-100">
                Welcome back, <span className="font-semibold text-indigo-700 dark:text-indigo-300">{userName}</span>! Stay organized and boost your productivity
              </p>
            )}
            {!userName && (
              <p className="mt-2 text-gray-600 dark:text-white text-lg animate-slide-up delay-100">
                Stay organized and boost your productivity
              </p>
            )}
          </div>

          {/* Stats Cards - with staggered animation */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 min-w-fit">
            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl p-4 border border-gray-200/50 dark:border-gray-700/50 shadow-sm animate-fade-in-scale delay-200 transition-all duration-300">
              <div className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">{totalTasks}</div>
              <div className="text-sm text-gray-600 dark:text-gray-300">Total Tasks</div>
            </div>
            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl p-4 border border-gray-200/50 dark:border-gray-700/50 shadow-sm animate-fade-in-scale delay-300 transition-all duration-300">
              <div className="text-2xl font-bold text-green-600 dark:text-green-400">{pendingTasks}</div>
              <div className="text-sm text-gray-600 dark:text-gray-300">Pending</div>
            </div>
            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl p-4 border border-gray-200/50 dark:border-gray-700/50 shadow-sm animate-fade-in-scale delay-400 transition-all duration-300">
              <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">{completedTasks}</div>
              <div className="text-sm text-gray-600 dark:text-gray-300">Completed</div>
            </div>
            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl p-4 border border-gray-200/50 dark:border-gray-700/50 shadow-sm animate-fade-in-scale delay-500 transition-all duration-300">
              <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">{completionRate}%</div>
              <div className="text-sm text-gray-600 dark:text-gray-300">Complete</div>
            </div>
          </div>
        </div>

        {/* Action Bar - with slide-in animation */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8 space-y-4 sm:space-y-0 animate-slide-in">
          <div className="flex items-center space-x-4">
            <button
              onClick={handleCreateTodo}
              className="flex items-center bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-xl hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-0.5 group"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 group-hover:scale-110 transition-transform duration-200" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
              Add New Task
            </button>

            {/* Filter Buttons - Removed functionality as requested */}
          </div>
        </div>

        {/* Progress Section - with reveal animation */}
        {totalTasks > 0 && (
          <div className="mb-8 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-2xl p-6 border border-gray-200/50 dark:border-gray-700/50 shadow-sm animate-reveal transition-all duration-300">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Your Progress</span>
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{completionRate}% Complete</span>
            </div>
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 overflow-hidden">
              <div
                className="bg-gradient-to-r from-green-400 to-green-600 h-3 rounded-full transition-all duration-1000 ease-out animate-progress-grow"
                style={{ width: `${completionRate}%` }}
              ></div>
            </div>
          </div>
        )}

        {/* Todo List - with staggered item animations */}
        {todos.length === 0 ? (
          <div className="text-center py-16 animate-fade-in">
            <div className="mx-auto h-24 w-24 rounded-full bg-gradient-to-r from-indigo-100 to-purple-100 dark:from-indigo-900/30 dark:to-purple-900/30 flex items-center justify-center mb-6 animate-bounce-once">
              <svg className="h-12 w-12 text-indigo-400 dark:text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h3 className="mt-4 text-xl font-medium text-gray-900 dark:text-white animate-fade-in delay-300">No tasks yet</h3>
            <p className="mt-2 text-gray-600 dark:text-gray-300 max-w-md mx-auto animate-fade-in delay-500">
              Get started by creating your first task. You'll be amazed at how much you can accomplish!
            </p>
            <div className="mt-8 animate-fade-in delay-700">
              <button
                onClick={handleCreateTodo}
                className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-xl text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 hover:-translate-y-0.5 group"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 group-hover:rotate-12 transition-transform duration-300" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
                </svg>
                Create Your First Task
              </button>
            </div>
          </div>
        ) : (
          <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-2xl shadow-lg border border-gray-200/50 dark:border-gray-700/50 overflow-hidden animate-fade-in-scale transition-all duration-300">
            <div className="p-6 border-b border-gray-200/50 dark:border-gray-700/50">
              <h2 className="text-lg font-semibold text-gray-800 dark:text-white animate-slide-up">Your Tasks</h2>
              <p className="text-sm text-gray-600 dark:text-gray-300 mt-1 animate-slide-up delay-100">Click on any task to edit or manage it</p>
            </div>
            <div className="p-6">
              <TodoList
                todos={todos}
                onEdit={handleEditTodo}
                onDelete={handleDeleteTodo}
                onToggle={handleToggleTodo}
              />
            </div>
          </div>
        )}
      </div>

      {showModal && (
        <TodoModal
          todo={currentTodo}
          onSave={handleSaveTodo}
          onClose={() => setShowModal(false)}
        />
      )}
    </div>
    </>
  );
}