import { createContext, useContext, useEffect, useState } from 'react';
import api from '../api';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Clear any previous auto-login session so Sign In screen is ALWAYS requested first
    localStorage.removeItem('learnlog_user');
    localStorage.removeItem('learnlog_token');
    setUser(null);
    setLoading(false);
  }, []);


  const authenticate = ({ token, user }) => {
    if (token) localStorage.setItem('learnlog_token', token);
    localStorage.setItem('learnlog_user', JSON.stringify(user));
    setUser(user);
  };

  const logout = () => {
    localStorage.removeItem('learnlog_token');
    localStorage.removeItem('learnlog_user');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, authenticate, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);

