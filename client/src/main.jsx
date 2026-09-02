import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './styles.css';
import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import ProtectedRoute from './components/ProtectedRoute';
import AuthPage from './pages/AuthPage';
import Dashboard from './pages/Dashboard';
import Lesson from './pages/Lesson';
import Quiz from './pages/Quiz';
import Analytics from './pages/Analytics';
import AuthorDesk from './pages/AuthorDesk';

const secure = (node, admin = false) => (
  <ProtectedRoute admin={admin}>{node}</ProtectedRoute>
);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <ThemeProvider>
        <AuthProvider>
          <Routes>
            <Route path="/login" element={<AuthPage />} />
            <Route path="/register" element={<AuthPage register />} />
            <Route path="/" element={secure(<Dashboard />)} />
            <Route path="/courses/:courseId/lessons/:lessonId" element={secure(<Lesson />)} />
            <Route path="/courses/:courseId/quiz/:lessonId" element={secure(<Quiz />)} />
            <Route path="/author" element={secure(<AuthorDesk />, true)} />
            <Route path="/analytics" element={secure(<Analytics />, true)} />
          </Routes>
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  </React.StrictMode>
);
