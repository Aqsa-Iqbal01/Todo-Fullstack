'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';

interface SessionContextType {
  token: string | null;
  setToken: (token: string | null) => void;
}

const SessionContext = createContext<SessionContextType | undefined>(undefined);

export const SessionProvider = ({ children }: { children: ReactNode }) => {
  const [token, setTokenState] = useState<string | null>(null);

  useEffect(() => {
    // Check for stored token on initial load
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      setTokenState(storedToken);
    }

    // Listen for storage changes (in case token is updated from another tab or component)
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'token') {
        setTokenState(e.newValue);
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  const setToken = (newToken: string | null) => {
    if (newToken) {
      localStorage.setItem('token', newToken);
      setTokenState(newToken);
    } else {
      localStorage.removeItem('token');
      setTokenState(null);
    }
  };

  return (
    <SessionContext.Provider value={{ token, setToken }}>
      {children}
    </SessionContext.Provider>
  );
};

export const useSession = () => {
  const context = useContext(SessionContext);
  if (context === undefined) {
    throw new Error('useSession must be used within a SessionProvider');
  }
  return context;
};