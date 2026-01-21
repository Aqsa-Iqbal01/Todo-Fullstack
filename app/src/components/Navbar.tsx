'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useTheme } from '@/contexts/ThemeContext';

const Navbar: React.FC = () => {
  const router = useRouter();
  const [userEmail, setUserEmail] = useState<string | null>(null);
  const { theme, toggleTheme } = useTheme();

  useEffect(() => {
    // Get user email from token or localStorage
    const token = localStorage.getItem('token');
    if (token) {
      try {
        // Decode JWT token to get user email
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(
          atob(base64)
            .split('')
            .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
            .join('')
        );
        const tokenData = JSON.parse(jsonPayload);
        setUserEmail(tokenData.sub || null); // 'sub' typically contains the user identifier (email)
      } catch (error) {
        console.error('Error decoding token:', error);
        // Fallback: try to get user info from localStorage if stored there
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
          try {
            const user = JSON.parse(storedUser);
            setUserEmail(user.email);
          } catch (parseError) {
            console.error('Error parsing stored user:', parseError);
          }
        }
      }
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user'); // Remove stored user info
    router.push('/login');
  };

  // Get user initial for avatar
  const userInitial = userEmail ? userEmail.charAt(0).toUpperCase() : '?';

  return (
    <nav className="bg-transparent backdrop-blur-md bg-opacity-10 border-b border-white/20 dark:border-gray-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0 flex items-center">
              <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-2 rounded-lg shadow-lg">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <span className="ml-3 text-xl font-bold text-gray-800 dark:text-white">Todo<span className="font-light text-gray-700 dark:text-gray-200 opacity-90 dark:opacity-100">Pro</span></span>
            </div>

            {/* Navigation Links */}
            <div className="ml-10 flex space-x-8">
              <Link href="/dashboard" className="text-gray-700 dark:text-gray-200 hover:text-indigo-600 dark:hover:text-indigo-300 transition-colors duration-200 font-medium">
                Dashboard
              </Link>
              <Link href="/chatbotPage
              
              
              
              " className="text-gray-700 dark:text-gray-200 hover:text-indigo-600 dark:hover:text-indigo-300 transition-colors duration-200 font-medium">
                AI Assistant
              </Link>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="hidden md:block text-sm text-gray-600 dark:text-gray-300">
              <span className="inline-flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1 text-green-500 dark:text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                Secured
              </span>
            </div>

            {/* Welcome Message */}
            {userEmail && (
              <div className="hidden md:block text-right">
                <div className="text-xs text-gray-700 dark:text-gray-200 font-medium truncate max-w-[120px]">{userEmail}</div>
                <div className="text-[0.6rem] text-gray-500 dark:text-gray-400">Welcome!</div>
              </div>
            )}

            {/* Theme Toggle Button */}
            <button
              onClick={toggleTheme}
              className="p-2 rounded-full bg-white/80 dark:bg-gray-700 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all duration-300 shadow-md hover:shadow-lg"
              aria-label="Toggle theme"
            >
              {theme === 'light' ? (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                </svg>
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              )}
            </button>

            <button
              onClick={handleLogout}
              className="flex items-center px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-200 bg-white/80 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all duration-300 border border-gray-300 dark:border-gray-600 shadow-md hover:shadow-lg"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-gray-700 dark:text-gray-200" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;