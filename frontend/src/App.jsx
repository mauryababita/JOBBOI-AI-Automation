import { useEffect, useState } from 'react';
import { Routes, Route, Link, Navigate, useLocation } from 'react-router-dom';
import {
  Activity,
  BarChart3,
  BellRing,
  Bookmark,
  Briefcase,
  FileCheck2,
  FileText,
  Files,
  LayoutDashboard,
  LogOut,
  Rocket,
  Search,
  Settings,
  ShieldCheck,
  Sparkles,
} from 'lucide-react';

import AuthPage from './pages/AuthPage';
import DashboardPage from './pages/DashboardPage';
import ResumePage from './pages/ResumePage';
import ResumeLibraryPage from './pages/ResumeLibraryPage';
import JobsPage from './pages/JobsPage';
import SkillGapPage from './pages/SkillGapPage';
import AutoApplyPage from './pages/AutoApplyPage';

const workflowItems = [
  { label: 'Resume', icon: FileText, to: '/resume' },
  { label: 'Search Jobs', icon: Search, to: '/jobs' },
  { label: 'Auto Apply', icon: Rocket, to: '/auto-apply' },
];

const resultItems = [
  { label: 'Resume Library', icon: Files, to: '/resume-library' },
  { label: 'Saved Jobs', icon: Bookmark, to: '/saved-jobs' },
  { label: 'Applications', icon: Briefcase, to: '/applications' },
  { label: 'Dashboard', icon: LayoutDashboard, to: '/' },
  { label: 'Skill Gap', icon: Activity, to: '/skill-gap' },
  { label: 'Cover Letters', icon: FileCheck2, to: '/cover-letters' },
  { label: 'Follow-ups', icon: BellRing, to: '/follow-ups' },
  { label: 'Analytics', icon: BarChart3, to: '/analytics' },
  { label: 'Settings', icon: Settings, to: '/settings' },
];

function NavGroup({ title, items }) {
  const location = useLocation();

  return (
    <div>
      <p className="mb-3 px-3 text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">{title}</p>
      <nav className="space-y-1">
        {items.map(({ label, icon: Icon, to }) => {
          const active = location.pathname === to;
          return (
            <Link
              key={label}
              to={to}
              className={`flex items-center gap-3 rounded-xl border px-3 py-2.5 text-sm font-semibold transition ${
                active
                  ? 'border-fuchsia-500/40 bg-fuchsia-500/15 text-fuchsia-200 shadow-[0_0_24px_rgba(217,70,239,0.18)]'
                  : 'border-transparent text-slate-400 hover:border-slate-800 hover:bg-slate-900/70 hover:text-slate-100'
              }`}
            >
              <Icon size={17} />
              <span>{label}</span>
            </Link>
          );
        })}
      </nav>
    </div>
  );
}

function Sidebar({ user, onLogout }) {
  return (
    <aside className="flex h-screen w-[280px] shrink-0 flex-col border-r border-slate-800/80 bg-[#070a14]/95">
      <div className="border-b border-slate-800/80 p-5">
        <div className="flex items-center gap-3">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-fuchsia-500 to-blue-500 text-white shadow-[0_0_32px_rgba(236,72,153,0.35)]">
            <Briefcase size={26} />
          </div>
          <div>
            <p className="text-xl font-black leading-none text-white">JobBot</p>
            <p className="text-lg font-black leading-tight text-slate-100">AI</p>
            <p className="text-[11px] font-semibold uppercase tracking-[0.22em] text-fuchsia-300">Auto Apply Engine</p>
          </div>
        </div>
        <div className="mt-4 inline-flex items-center gap-2 rounded-full border border-fuchsia-500/30 bg-fuchsia-500/10 px-3 py-1 text-xs font-semibold text-fuchsia-200">
          <Sparkles size={13} />
          AI
        </div>
      </div>

      <div className="flex-1 space-y-7 overflow-y-auto p-4">
        <NavGroup title="Workflow" items={workflowItems} />
        <NavGroup title="Results" items={resultItems} />
      </div>

      <div className="border-t border-slate-800/80 p-4">
        <div className="space-y-2 rounded-2xl border border-slate-800 bg-slate-950/70 p-3 text-xs">
          <div className="flex items-center gap-2 text-amber-300">
            <span className="h-2 w-2 rounded-full bg-amber-400" />
            <span>No platform connected</span>
          </div>
        </div>
        <button
          onClick={onLogout}
          className="mt-3 flex w-full items-center justify-center gap-2 rounded-xl border border-slate-800 px-3 py-2 text-sm font-semibold text-slate-300 transition hover:bg-slate-900"
        >
          <LogOut size={16} />
          Log out
        </button>
      </div>
    </aside>
  );
}

function TopBar({ user }) {
  return (
    <header className="sticky top-0 z-20 border-b border-slate-800/80 bg-[#070a14]/90 px-6 py-4 backdrop-blur">
      <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex flex-wrap items-center gap-3">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1.5 text-sm font-semibold text-emerald-300">
            <span className="h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_12px_rgba(52,211,153,0.8)]" />
            Ready
          </div>
          <div className="inline-flex items-center gap-2 rounded-full border border-fuchsia-500/30 bg-fuchsia-500/10 px-3 py-1.5 text-sm font-semibold text-fuchsia-200">
            <ShieldCheck size={15} />
            Session: {(user?.name || 'Demo User').toUpperCase()}
          </div>
        </div>
        <div className="flex items-center gap-3">
          <div className="hidden rounded-2xl border border-slate-800 bg-slate-950/70 px-4 py-2 text-sm text-slate-400 md:block">
            Search jobs, skills, companies...
          </div>
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-fuchsia-500 to-blue-500 text-sm font-black text-white">
            {(user?.name || 'D').charAt(0).toUpperCase()}
          </div>
        </div>
      </div>
    </header>
  );
}

function PlaceholderPage({ title, subtitle }) {
  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-950/70 p-6 shadow-[0_0_40px_rgba(15,23,42,0.35)]">
      <p className="text-sm font-semibold uppercase tracking-[0.2em] text-fuchsia-300">JobBot AI</p>
      <h1 className="mt-2 text-3xl font-black text-white">{title}</h1>
      <p className="mt-3 max-w-2xl text-sm text-slate-400">{subtitle}</p>
    </div>
  );
}

function AppLayout({ user, token, onLogout }) {
  return (
    <div className="flex min-h-screen bg-[#050714] text-slate-100">
      <Sidebar user={user} onLogout={onLogout} />
      <div className="min-w-0 flex-1">
        <TopBar user={user} />
        <main className="mx-auto max-w-[1480px] p-5 md:p-6">
          <Routes>
            <Route path="/" element={<DashboardPage token={token} />} />
            <Route path="/resume" element={<ResumePage token={token} />} />
            <Route path="/resume-library" element={<ResumeLibraryPage token={token} />} />
            <Route path="/ats" element={<ResumePage token={token} />} />
            <Route path="/jobs" element={<JobsPage token={token} />} />
            <Route path="/skill-gap" element={<SkillGapPage token={token} />} />
            <Route path="/auto-apply" element={<AutoApplyPage token={token} user={user} />} />
            <Route path="/saved-jobs" element={<PlaceholderPage title="Saved Jobs" subtitle="Saved jobs from search results appear here for later review." />} />
            <Route path="/applications" element={<PlaceholderPage title="Applications" subtitle="Track discovered, ready-to-apply, submitted, interview, rejected, and manual-action states." />} />
            <Route path="/cover-letters" element={<PlaceholderPage title="Cover Letters" subtitle="Generated drafts are saved by job so you can review them before using them." />} />
            <Route path="/follow-ups" element={<PlaceholderPage title="Follow-ups" subtitle="Schedule reminders and keep response tracking organized by application." />} />
            <Route path="/analytics" element={<DashboardPage token={token} />} />
            <Route path="/versions" element={<PlaceholderPage title="Resume Versions" subtitle="Compare resume versions and ATS-style score improvements over time." />} />
            <Route path="/settings" element={<PlaceholderPage title="Settings" subtitle="Configure API keys, uploads, safe automation permissions, and source adapter settings." />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default function App() {
  const [authState, setAuthState] = useState(() => {
    const stored = localStorage.getItem('jobbot-auth');
    return stored ? JSON.parse(stored) : null;
  });

  useEffect(() => {
    if (authState) {
      localStorage.setItem('jobbot-auth', JSON.stringify(authState));
    } else {
      localStorage.removeItem('jobbot-auth');
    }
  }, [authState]);

  const handleAuth = (data) => {
    setAuthState({ token: data.token, user: data.user });
  };

  const handleLogout = () => {
    setAuthState(null);
  };

  if (!authState) {
    return <AuthPage onAuth={handleAuth} />;
  }

  return <AppLayout user={authState.user} token={authState.token} onLogout={handleLogout} />;
}
