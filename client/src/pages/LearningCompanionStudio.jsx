import { useEffect } from 'react';

export default function LearningCompanionStudio() {
  useEffect(() => {
    window.location.replace('/Learning_Companion_Studio.html' + window.location.search + window.location.hash);
  }, []);

  return (
    <div className="w-full min-h-[100dvh] flex flex-col items-center justify-center bg-slate-50 p-6 text-center">
      <div className="h-12 w-12 rounded-2xl bg-teal-700 flex items-center justify-center text-white font-black text-xl mb-3 shadow-lg shadow-teal-700/20 animate-pulse">
        LC
      </div>
      <h2 className="text-base font-extrabold text-slate-800">Learning Companion Studio</h2>
      <p className="text-xs text-slate-500 mt-1">Loading mobile-optimized training platform...</p>
      <a 
        href="/Learning_Companion_Studio.html" 
        className="mt-4 px-4 py-2 bg-teal-700 text-white rounded-xl text-xs font-bold hover:bg-teal-600 transition-all shadow-sm"
      >
        Click here if not redirected automatically →
      </a>
    </div>
  );
}
