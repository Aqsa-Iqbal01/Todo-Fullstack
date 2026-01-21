/* eslint-disable react/no-unescaped-entities */
'use client';

import { useSession } from '@/contexts/SessionContext';
import ChatbotInterface from '../../components/ChatbotInterface';
import Navbar from '../../components/Navbar';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

const ChatbotPageContent = () => {
  const { token } = useSession();
  const router = useRouter();
  const [hasCheckedAuth, setHasCheckedAuth] = useState(false);
  const [isAuthorized, setIsAuthorized] = useState(false);

  useEffect(() => {
    // Check auth status immediately
    const checkAuth = () => {
      const storedToken = localStorage.getItem('token');
      const isValid = Boolean(token || storedToken);

      if (isValid) {
        setIsAuthorized(true);
      } else {
        router.push('/login');
      }
      setHasCheckedAuth(true);
    };

    // Run immediately
    checkAuth();

    // Also listen for storage changes (in case token is updated from another tab)
    const handleStorageChange = () => {
      const storedToken = localStorage.getItem('token');
      const isValid = Boolean(token || storedToken);

      if (!isValid) {
        router.push('/login');
      } else {
        setIsAuthorized(true);
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [token, router]);

  // Don't render anything until auth is checked
  if (!hasCheckedAuth) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-indigo-600"></div>
          <p className="mt-4 text-lg text-gray-700 dark:text-gray-300">Loading AI Assistant...</p>
        </div>
      </div>
    );
  }

  // If not authorized, render nothing (should have redirected by now)
  if (!isAuthorized) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <Navbar />
      <main className="container mx-auto py-8 px-4">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">AI Todo Assistant</h1>
          <p className="text-gray-600 dark:text-gray-300">Manage your todos using natural language</p>
        </div>

        <div className="flex justify-center">
          <ChatbotInterface />
        </div>

        <div className="mt-8 max-w-2xl mx-auto text-left bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm p-6 rounded-xl shadow-lg border border-gray-200/50 dark:border-gray-700/50">
          <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-white">How to use the AI Assistant:</h2>
          <ul className="list-disc pl-5 space-y-2 text-gray-600 dark:text-gray-300">
            <li>Add todos: "Add buy groceries to my list"</li>
            <li>List todos: "Show my todos" or "What do I have to do?"</li>
            <li>Update todos: "Update buy groceries to complete" or "Change due date of finish report to Friday"</li>
            <li>Delete todos: "Delete buy groceries" or "Remove the meeting"</li>
          </ul>
        </div>
      </main>
    </div>
  );
};

const ChatbotPage = () => {
  return (
    <ChatbotPageContent />
  );
};

export default ChatbotPage;