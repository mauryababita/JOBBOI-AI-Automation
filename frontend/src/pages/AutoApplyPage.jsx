import { useState } from 'react';
import { Play, ShieldAlert } from 'lucide-react';

export default function AutoApplyPage({ user }) {
  const [applying, setApplying] = useState(false);

  const logs = applying
    ? [
      'Opening selected job workflow',
      'Checking source permissions',
      'Filling name from candidate profile',
      'Looking for application form',
      'Manual review required before submit',
    ]
    : [
      'Bot ready',
      '3 selected jobs waiting',
      'Safe mode enabled',
    ];

  return (
    <div className="grid gap-6 xl:grid-cols-[360px_1fr]">
      <section className="space-y-5">
        <div className="rounded-3xl border border-slate-800 bg-slate-950/70 p-5">
          <h1 className="text-2xl font-black text-white">Apply Settings</h1>
          <div className="mt-5 space-y-4">
            {[
              ['Your First Name', user?.name?.split(' ')[0] || 'Demo'],
              ['Your Last Name', user?.name?.split(' ').slice(1).join(' ') || 'User'],
              ['Phone Number', '+91 98765 43210'],
              ['Years of Experience', '1'],
            ].map(([label, value]) => (
              <label key={label} className="block">
                <span className="text-sm font-bold text-slate-400">{label}</span>
                <input defaultValue={value} className="mt-2 w-full rounded-2xl border border-slate-800 bg-slate-900 px-4 py-3 text-sm font-semibold text-white outline-none focus:border-fuchsia-500" />
              </label>
            ))}

            <div>
              <p className="mb-2 text-sm font-bold text-slate-400">Minimum Match Score</p>
              <div className="flex flex-wrap gap-2">
                {['All', '40%+', '60%+', '80%+'].map((item, index) => (
                  <span key={item} className={`rounded-full border px-3 py-1.5 text-xs font-black ${index === 0 ? 'border-fuchsia-500/60 bg-fuchsia-500/15 text-fuchsia-200' : 'border-slate-800 bg-slate-900 text-slate-400'}`}>{item}</span>
                ))}
              </div>
            </div>

            <div className="border-t border-slate-800 pt-4">
              <p className="text-sm font-bold text-white">Selected Jobs</p>
              <p className="text-sm text-slate-500">3 jobs selected</p>
            </div>

            <button onClick={() => setApplying(true)} className="flex w-full items-center justify-center gap-2 rounded-2xl bg-gradient-to-r from-fuchsia-600 to-pink-500 px-4 py-3 text-sm font-black text-white shadow-[0_0_30px_rgba(236,72,153,0.26)]">
              <Play size={16} />
              {applying ? 'Applying...' : 'Start Applying'}
            </button>
          </div>
        </div>

        <div className="rounded-3xl border border-slate-800 bg-slate-950/70 p-5">
          <h2 className="text-lg font-black text-white">Bot Activity</h2>
          <div className="mt-4 rounded-2xl border border-slate-800 bg-[#070b15] p-3 font-mono text-xs">
            <div className="mb-3 flex gap-2">
              <span className="h-3 w-3 rounded-full bg-rose-400" />
              <span className="h-3 w-3 rounded-full bg-amber-400" />
              <span className="h-3 w-3 rounded-full bg-emerald-400" />
            </div>
            <div className="space-y-2">
              {logs.map((log, index) => (
                <p key={log} className="text-blue-300">
                  {new Date(Date.now() + index * 1000).toLocaleTimeString()} {log}
                </p>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="rounded-3xl border border-slate-800 bg-slate-950/70 p-5">
        <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
          <div>
            <h1 className="text-2xl font-black text-white">Application Results</h1>
            <p className="mt-1 text-sm text-slate-400">Results appear here as the bot prepares each application.</p>
          </div>
          <span className="rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1.5 text-sm font-bold text-emerald-300">Live Scraping</span>
        </div>

        <div className="mt-8 rounded-3xl border border-amber-500/20 bg-amber-500/10 p-5">
          <div className="flex items-start gap-3">
            <ShieldAlert className="mt-1 text-amber-300" size={22} />
            <div>
              <p className="font-black text-amber-100">Manual review required before final submit</p>
              <p className="mt-2 max-w-2xl text-sm leading-6 text-amber-100/75">
                JobBot can prepare application data and pause at review. It will not bypass CAPTCHA, MFA, rate limits, or silently submit applications without configured permission.
              </p>
            </div>
          </div>
        </div>

        {applying && (
          <div className="mt-5 space-y-3">
            {['Claude Certified Developer', 'Python Backend Engineer', 'Full Stack Engineer'].map((title, index) => (
              <div key={title} className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-black text-white">{title}</p>
                    <p className="text-sm text-slate-500">Prepared for review</p>
                  </div>
                  <span className="rounded-full bg-fuchsia-500/15 px-3 py-1 text-xs font-black text-fuchsia-200">{index === 0 ? 'NEEDS_USER_ACTION' : 'READY_TO_APPLY'}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
