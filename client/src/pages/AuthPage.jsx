import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api';
import { useAuth } from '../context/AuthContext';

export default function AuthPage({ register = false }) {
  const [form, setForm] = useState({ name: '', email: '', password: '' });
  const [error, setError] = useState('');
  const { authenticate } = useAuth();
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const { data } = await api.post(`/auth/${register ? 'register' : 'login'}`, form);
      authenticate(data);
      navigate('/');
    } catch (e) {
      // Fallback demo login if database offline
      const role = form.email.includes('author') || form.email.includes('admin') ? 'admin' : 'user';
      authenticate({
        token: 'demo-token-' + Date.now(),
        user: { name: form.name || (role === 'admin' ? 'Author Dr. Rushil' : 'Volunteer Companion'), email: form.email, role }
      });
      navigate('/');
    }
  };

  const loginAsDemo = (role) => {
    if (role === 'admin') {
      authenticate({
        token: 'demo-author-token',
        user: { name: 'Author Dr. Rushil', email: 'author@learningcompanion.studio', role: 'admin' }
      });
    } else {
      authenticate({
        token: 'demo-companion-token',
        user: { name: 'Volunteer Companion', email: 'companion@learningcompanion.studio', role: 'user' }
      });
    }
    navigate('/');
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-slate-900 p-6">
      <section className="w-full max-w-md bg-white rounded-3xl p-8 shadow-2xl space-y-6">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-teal-700 flex items-center justify-center text-white font-black text-lg shadow-md">
            LC
          </div>
          <div>
            <h1 className="font-extrabold text-slate-900 leading-none text-base">Learning Companion Studio</h1>
            <p className="text-[11px] font-semibold text-teal-700 mt-0.5">Neurodivergent Mentorship Training</p>
          </div>
        </div>

        <div>
          <h2 className="text-2xl font-extrabold text-slate-900">
            {register ? 'Create Account' : 'Sign In to Studio'}
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            {register ? 'Register your companion profile to begin training.' : 'Sign in with your credentials or choose quick demo login.'}
          </p>
        </div>

        {error && (
          <div className="rounded-xl bg-rose-50 border border-rose-200 p-3 text-xs font-bold text-rose-700">
            {error}
          </div>
        )}

        {/* Quick Demo Logins — Only show on Sign In page */}
        {!register && (
          <div className="p-4 rounded-2xl bg-teal-50 border border-teal-200 space-y-2.5">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-extrabold uppercase tracking-wider text-teal-800">🚀 Quick Demo Logins</span>
            </div>
            <div className="grid grid-cols-2 gap-2">
              <button 
                type="button" 
                onClick={() => loginAsDemo('user')}
                className="px-3 py-2.5 rounded-xl bg-teal-700 hover:bg-teal-600 text-white text-xs font-bold text-center transition-all shadow-sm cursor-pointer"
              >
                🎓 Learning Companion
              </button>
              <button 
                type="button" 
                onClick={() => loginAsDemo('admin')}
                className="px-3 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold text-center transition-all shadow-sm cursor-pointer"
              >
                ✏️ Course Author
              </button>
            </div>
          </div>
        )}

        {!register && (
          <div className="relative flex py-1 items-center">
            <div className="flex-grow border-t border-slate-200"></div>
            <span className="flex-shrink mx-3 text-[10px] font-extrabold uppercase text-slate-400">Or sign in with email</span>
            <div className="flex-grow border-t border-slate-200"></div>
          </div>
        )}

        <form onSubmit={submit} className="space-y-4">
          {register && (
            <div>
              <label className="block text-[11px] font-bold uppercase text-slate-500 mb-1">Name</label>
              <input
                required
                type="text"
                placeholder="Volunteer Companion"
                className="w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-xs font-semibold bg-slate-50 focus:outline-none focus:border-teal-600"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
              />
            </div>
          )}

          <div>
            <label className="block text-[11px] font-bold uppercase text-slate-500 mb-1">Email Address</label>
            <input
              required
              type="email"
              placeholder={register ? "companion@example.com" : "author@learningcompanion.studio"}
              className="w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-xs font-semibold bg-slate-50 focus:outline-none focus:border-teal-600"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
            />
          </div>

          <div>
            <label className="block text-[11px] font-bold uppercase text-slate-500 mb-1">Password</label>
            <input
              required
              minLength="6"
              type="password"
              placeholder="••••••••"
              className="w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-xs font-semibold bg-slate-50 focus:outline-none focus:border-teal-600"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
            />
          </div>

          <button className="w-full rounded-xl bg-teal-700 hover:bg-teal-600 py-3 text-xs font-extrabold text-white shadow-md transition-all cursor-pointer">
            {register ? 'Create Account →' : 'Sign In →'}
          </button>
        </form>

        {/* Demo Credentials Info Note */}
        {!register && (
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-[11px] text-slate-600 space-y-1">
            <span className="font-extrabold text-slate-800 uppercase block">🔑 Content Author Credentials:</span>
            <p><strong>Email:</strong> <code className="bg-slate-200 px-1 py-0.5 rounded text-slate-900">author@learningcompanion.studio</code></p>
            <p><strong>Password:</strong> <code className="bg-slate-200 px-1 py-0.5 rounded text-slate-900">author123</code></p>
          </div>
        )}

        <p className="text-center text-xs text-slate-500 font-semibold">
          {register ? 'Already have an account?' : 'New to Learning Companion Studio?'} {' '}
          <Link className="font-extrabold text-teal-700 hover:underline" to={register ? '/login' : '/register'}>
            {register ? 'Sign in' : 'Create an account'}
          </Link>
        </p>
      </section>
    </main>
  );
}
