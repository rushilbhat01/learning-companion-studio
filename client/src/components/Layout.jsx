import { Link, NavLink, useNavigate } from 'react-router-dom';
import { BookOpen, BarChart3, LogOut, Sun, Moon, Edit3 } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

export default function Layout({ children }) {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const leave = () => {
    logout();
    navigate('/login');
  };

  const navLinkClass = ({ isActive }) =>
    `flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200 ${
      isActive
        ? 'bg-brand/10 text-brand dark:bg-indigo-500/10 dark:text-indigo-400'
        : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
    }`;

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 flex flex-col transition-colors duration-200">
      <header className="sticky top-0 z-50 border-b border-slate-100 dark:border-slate-800/80 bg-white/70 dark:bg-slate-900/70 backdrop-blur-md">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-5">
          <Link to="/" className="flex items-center gap-2.5 text-xl font-bold tracking-tight text-slate-900 dark:text-white">
            <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-brand dark:bg-indigo-600 text-white shadow-md shadow-brand/10 dark:shadow-none">
              <BookOpen size={18} />
            </span>
            <span>Learning Companion Studio</span>
          </Link>
          
          <nav className="flex items-center gap-3">
            <NavLink to="/" end className={navLinkClass}>
              Dashboard
            </NavLink>
            
            {user?.role === 'admin' && (
              <>
                <NavLink to="/author" className={navLinkClass}>
                  <Edit3 size={15} />
                  <span>Author Desk</span>
                </NavLink>
                <NavLink to="/analytics" className={navLinkClass}>
                  <BarChart3 size={15} />
                  <span>Analytics</span>
                </NavLink>
              </>
            )}

            <div className="h-4 w-px bg-slate-200 dark:bg-slate-800 mx-1 hidden sm:block" />

            <span className="hidden text-slate-500 dark:text-slate-400 text-sm font-medium sm:inline">
              {user?.name}
            </span>

            <button
              onClick={toggleTheme}
              title={theme === 'light' ? 'Switch to Dark Mode' : 'Switch to Light Mode'}
              className="p-2 rounded-lg text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            >
              {theme === 'light' ? <Moon size={16} /> : <Sun size={16} />}
            </button>

            <button
              onClick={leave}
              title="Sign out"
              className="p-2 rounded-lg text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-rose-600 dark:hover:text-rose-400 transition-colors"
            >
              <LogOut size={16} />
            </button>
          </nav>
        </div>
      </header>

      <main className="mx-auto w-full max-w-6xl flex-grow px-5 py-8">
        {children}
      </main>

      <footer className="border-t border-slate-100 dark:border-slate-900 bg-white dark:bg-slate-950/40 py-6 text-center text-xs text-slate-400 dark:text-slate-600">
        <div className="mx-auto max-w-6xl px-5">
          <p>© {new Date().getFullYear()} Learning Companion Studio & Training Platform.</p>
        </div>
      </footer>
    </div>
  );
}
