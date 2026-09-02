import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import AuthorDesk from './AuthorDesk';

export default function LearningCompanionStudio() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const isAdmin = user?.role === 'admin';
  const [viewMode, setViewMode] = useState(isAdmin ? 'live-author' : 'studio');

  const handleSignOut = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-900">
      {/* Top Authentication Bar */}
      <div className="bg-slate-950 text-white px-6 py-2.5 border-b border-slate-800 flex items-center justify-between text-xs shadow-md">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="font-bold text-slate-300">
              {isAdmin ? '👑 Author Account:' : '👤 Companion Account:'}{' '}
              <strong className="text-white">{user?.name || 'User'}</strong> ({user?.email})
            </span>
          </div>

          {isAdmin && (
            <div className="flex items-center gap-1 bg-slate-900 p-1 rounded-xl border border-slate-800 ml-4">
              <button 
                onClick={() => setViewMode('live-author')} 
                className={`px-3 py-1 rounded-lg font-bold text-xs transition-all ${viewMode === 'live-author' ? 'bg-indigo-600 text-white shadow-sm' : 'text-slate-400 hover:text-white'}`}
              >
                📊 Live DB Authoring Desk
              </button>
              <button 
                onClick={() => setViewMode('studio')} 
                className={`px-3 py-1 rounded-lg font-bold text-xs transition-all ${viewMode === 'studio' ? 'bg-teal-700 text-white shadow-sm' : 'text-slate-400 hover:text-white'}`}
              >
                🎓 Companion Studio Preview
              </button>
            </div>
          )}
        </div>

        <button 
          onClick={handleSignOut} 
          className="px-3.5 py-1 rounded-lg bg-rose-500/20 hover:bg-rose-600 text-rose-300 hover:text-white font-bold transition-all border border-rose-500/30 cursor-pointer"
        >
          🚪 Sign Out
        </button>
      </div>

      {/* Content View */}
      {viewMode === 'live-author' ? (
        <div className="flex-grow bg-slate-50 dark:bg-slate-950 p-6">
          <AuthorDesk />
        </div>
      ) : (
        <iframe 
          src="/Learning_Companion_Studio.html" 
          title="Learning Companion Studio" 
          className="w-full flex-grow border-0 shadow-none m-0 p-0 min-h-[calc(100vh-45px)]"
        />
      )}
    </div>
  );
}
