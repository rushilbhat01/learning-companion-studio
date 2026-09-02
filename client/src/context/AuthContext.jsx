import { createContext, useContext, useEffect, useState } from 'react';
import api from '../api';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const savedUser = localStorage.getItem('learnlog_user');
    if (savedUser) {
      try {
        setUser(JSON.parse(savedUser));
        setLoading(false);
        return;
      } catch (e) {
        localStorage.removeItem('learnlog_user');
      }
    }

    api.get('/auth/me')
      .then(({ data }) => {
        setUser(data.user);
        localStorage.setItem('learnlog_user', JSON.stringify(data.user));
      })
      .catch(() => {
        localStorage.removeItem('learnlog_token');
        localStorage.removeItem('learnlog_user');
      })
      .finally(() => setLoading(false));
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

