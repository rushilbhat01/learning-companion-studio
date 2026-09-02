import React from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export default function LearningCompanionStudio() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleSignOut = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-900">
      {/* Top Authentication Bar */}
      <div className="bg-slate-950 text-white px-6 py-2.5 border-b border-slate-800 flex items-center justify-between text-xs shadow-md">
        <div className="flex items-center gap-2">
          <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span className="font-bold text-slate-300">
            Authenticated User: <strong className="text-white">{user?.name || 'Volunteer Companion'}</strong> ({user?.email || 'companion@learningcompanion.studio'})
          </span>
        </div>
        <button 
          onClick={handleSignOut} 
          className="px-3.5 py-1 rounded-lg bg-rose-500/20 hover:bg-rose-600 text-rose-300 hover:text-white font-bold transition-all border border-rose-500/30 cursor-pointer"
        >
          🚪 Sign Out
        </button>
      </div>

      {/* Studio Embedded */}
      <iframe 
        src="/Learning_Companion_Studio.html" 
        title="Learning Companion Studio" 
        className="w-full flex-grow border-0 shadow-none m-0 p-0 min-h-[calc(100vh-42px)]"
      />
    </div>
  );
}
