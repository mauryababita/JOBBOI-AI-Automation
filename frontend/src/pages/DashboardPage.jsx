import { useEffect, useState } from 'react';
import { ArrowRight, BriefcaseBusiness, CalendarDays, CheckCircle2, Rocket } from 'lucide-react';
import { getAnalytics } from '../services/api';

const emptyAnalytics = {
  total_jobs_found: 0,
  matched_jobs: 0,
  applications: 0,
  interview_responses: 0,
  saved_jobs: 0,
  average_match_score: 0,
  response_rate: 0,
  applications_by_platform: [],
  applications_by_status: [],
};

function StatCard({ label, value, detail, icon: Icon, tone }) {
  const gradient = tone === 'blue'
    ? 'from-blue-600 to-cyan-500'
    : tone === 'purple'
      ? 'from-violet-600 to-fuchsia-500'
      : 'from-fuchsia-600 to-pink-500';

  return (
    <div className={`rounded-3xl border border-slate-800 bg-gradient-to-br ${gradient} p-5 shadow-[0_0_36px_rgba(236,72,153,0.14)]`}>
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-sm font-semibold text-white/80">{label}</p>
          <p className="mt-3 text-3xl font-black text-white">{value}</p>
          <p className="mt-2 text-xs font-semibold text-white/70">{detail}</p>
        </div>
        <div className="rounded-2xl bg-white/15 p-3 text-white">
          <Icon size={24} />
        </div>
      </div>
    </div>
  );
}

function Panel({ title, children, action }) {
  return (
    <section className="rounded-3xl border border-slate-800 bg-slate-950/70 p-5 shadow-[0_0_40px_rgba(15,23,42,0.35)]">
      <div className="mb-5 flex items-center justify-between gap-3">
        <h2 className="text-lg font-black text-white">{title}</h2>
        {action}
      </div>
      {children}
    </section>
  );
}

export default function DashboardPage({ token }) {
  const [analytics, setAnalytics] = useState(emptyAnalytics);

  useEffect(() => {
    if (!token) return;
    getAnalytics(token)
      .then((result) => setAnalytics({ ...emptyAnalytics, ...result.data }))
      .catch(() => setAnalytics(emptyAnalytics));
  }, [token]);

  const hasActivity = analytics.applications > 0 || analytics.saved_jobs > 0 || analytics.total_jobs_found > 0;

  return (
    <div className="space-y-6">
      <div className="grid gap-4 xl:grid-cols-4">
        <StatCard label="Jobs Found" value={analytics.total_jobs_found} detail="live normalized listings" icon={BriefcaseBusiness} tone="pink" />
        <StatCard label="Applications" value={analytics.applications} detail="tracked in pipeline" icon={Rocket} tone="blue" />
        <StatCard label="Saved Jobs" value={analytics.saved_jobs} detail="ready for review" icon={CalendarDays} tone="purple" />
        <div className="rounded-3xl border border-slate-800 bg-slate-950/70 p-5">
          <p className="text-sm font-semibold text-slate-400">Success Rate</p>
          <p className="mt-3 text-3xl font-black text-white">{analytics.response_rate}%</p>
          {analytics.response_rate > 0 ? (
            <div className="mt-4 flex h-16 items-end gap-2">
              {[analytics.response_rate].map((height, index) => (
                <span key={index} className="w-full rounded-t-lg bg-gradient-to-t from-blue-600 to-fuchsia-500" style={{ height: Math.max(8, height) }} />
              ))}
            </div>
          ) : (
            <p className="mt-4 text-sm text-slate-500">No response data yet.</p>
          )}
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.5fr_360px]">
        <section className="overflow-hidden rounded-3xl border border-slate-800 bg-slate-950/70 shadow-[0_0_40px_rgba(15,23,42,0.35)]">
          <div className="grid gap-5 p-6 lg:grid-cols-[1fr_300px]">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.2em] text-fuchsia-300">Welcome back</p>
              <h1 className="mt-3 text-4xl font-black leading-tight text-white">Your AI job assistant is working for you</h1>
              <p className="mt-4 max-w-2xl text-sm leading-6 text-slate-400">
                Upload a resume, scrape permitted job sources, score every role, generate draft cover letters, and pause before final application submission.
              </p>
              <a href="/jobs" className="mt-6 inline-flex items-center gap-2 rounded-2xl bg-gradient-to-r from-fuchsia-600 to-pink-500 px-5 py-3 text-sm font-black text-white shadow-[0_0_30px_rgba(236,72,153,0.32)]">
                Find Better Jobs
                <ArrowRight size={17} />
              </a>
            </div>
            <div className="relative flex min-h-56 items-center justify-center rounded-3xl border border-fuchsia-500/20 bg-slate-900/70">
              <div className="absolute inset-x-8 bottom-8 h-2 rounded-full bg-blue-500/40 blur-md" />
              <div className="relative flex h-28 w-28 items-center justify-center rounded-[2rem] bg-gradient-to-br from-fuchsia-500 to-blue-500 text-white shadow-[0_0_50px_rgba(59,130,246,0.35)]">
                <Rocket size={54} />
              </div>
            </div>
          </div>
        </section>

        <Panel title="Resume ATS Score">
          <div className="flex flex-col items-center">
            <div className="flex h-44 w-44 items-center justify-center rounded-full border-[14px] border-blue-500 bg-slate-950 shadow-[0_0_35px_rgba(59,130,246,0.28)]">
              <div className="text-center">
                <p className="text-5xl font-black text-white">{analytics.average_match_score || 0}</p>
                <p className="text-sm font-semibold text-slate-500">/100</p>
              </div>
            </div>
            <p className="mt-4 font-black text-white">{analytics.average_match_score ? 'Resume score available' : 'No resume score yet'}</p>
            <p className="mt-1 text-center text-sm text-slate-400">Upload and analyze a resume to populate this score.</p>
          </div>
        </Panel>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1fr_1fr_360px]">
        <Panel title="Recent Applications" action={<button className="text-sm font-semibold text-fuchsia-300">View all</button>}>
          <div className="space-y-3">
            <p className="rounded-2xl border border-slate-800 bg-slate-900/60 p-4 text-sm text-slate-500">
              No applications yet.
            </p>
          </div>
        </Panel>

        <Panel title="Application Analytics">
          {hasActivity ? (
            <div className="space-y-3">
              {analytics.applications_by_status.map((item) => (
                <div key={item.name} className="rounded-2xl border border-slate-800 bg-slate-900/60 p-3">
                  <div className="flex items-center justify-between text-sm">
                    <span className="font-bold text-slate-200">{item.name}</span>
                    <span className="font-black text-fuchsia-200">{item.value}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex h-64 items-center justify-center rounded-2xl border border-dashed border-slate-800 text-sm text-slate-500">
              No analytics data yet.
            </div>
          )}
        </Panel>

        <Panel title="Bot Activity">
          <div className="space-y-3 font-mono text-xs">
            <div className="rounded-xl border border-slate-800 bg-[#080d18] p-3 text-slate-500">
              No automation activity yet.
            </div>
          </div>
          <div className="mt-5 rounded-2xl border border-emerald-500/20 bg-emerald-500/10 p-3 text-sm text-emerald-200">
            <div className="flex items-center gap-2 font-bold">
              <CheckCircle2 size={16} />
              Safe automation mode enabled
            </div>
            <p className="mt-2 text-xs text-emerald-200/80">CAPTCHA, MFA, and unsupported questions pause for manual action.</p>
          </div>
        </Panel>
      </div>
    </div>
  );
}
