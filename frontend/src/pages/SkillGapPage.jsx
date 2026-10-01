import { useState } from 'react';
import { CheckCircle2, CircleDashed, XCircle } from 'lucide-react';
import { analyzeJobDescription } from '../services/api';

function SkillList({ title, items, icon: Icon, tone }) {
  const toneClass = tone === 'green' ? 'text-emerald-300 bg-emerald-500/10' : tone === 'red' ? 'text-rose-300 bg-rose-500/10' : 'text-amber-300 bg-amber-500/10';
  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-950/70 p-5">
      <h2 className="mb-4 text-sm font-black uppercase tracking-[0.16em] text-slate-500">{title}</h2>
      <div className="space-y-2">
        {items.length === 0 ? (
          <p className="text-sm text-slate-500">Nothing detected yet.</p>
        ) : items.map((item) => (
          <div key={item} className={`flex items-center gap-2 rounded-xl px-3 py-2 text-sm font-bold ${toneClass}`}>
            <Icon size={16} />
            <span>{item}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function SkillGapPage({ token }) {
  const [jobDescription, setJobDescription] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!token || !jobDescription.trim()) return;
    setLoading(true);
    setError('');
    try {
      const response = await analyzeJobDescription({ jobDescription, token });
      setResult(response.data);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  };

  const analysis = result?.analysis;
  const match = result?.match;

  return (
    <div className="space-y-6">
      <div className="grid gap-6 xl:grid-cols-[1fr_360px]">
        <div className="rounded-3xl border border-slate-800 bg-slate-950/70 p-5">
          <div className="mb-4">
            <p className="text-sm font-black uppercase tracking-[0.2em] text-fuchsia-300">Skill Gap</p>
            <h1 className="mt-2 text-3xl font-black text-white">Analyze a Job Description</h1>
          </div>
          <textarea
            value={jobDescription}
            onChange={(event) => setJobDescription(event.target.value)}
            className="min-h-72 w-full resize-y rounded-3xl border border-slate-800 bg-slate-900 p-4 text-sm text-slate-200 outline-none focus:border-fuchsia-500"
            placeholder="Paste a job description..."
          />
          {error && <div className="mt-4 rounded-xl border border-rose-500/30 bg-rose-500/10 p-3 text-sm text-rose-200">{error}</div>}
          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="mt-4 rounded-2xl bg-gradient-to-r from-fuchsia-600 to-pink-500 px-5 py-3 text-sm font-black text-white shadow-[0_0_30px_rgba(236,72,153,0.24)] disabled:opacity-60"
          >
            {loading ? 'Analyzing...' : 'Analyze Skill Gap'}
          </button>
        </div>

        <div className="rounded-3xl border border-slate-800 bg-slate-950/70 p-5">
          <p className="text-sm font-bold text-slate-500">Match Score</p>
          {match ? (
            <>
              <div className="mt-4 flex h-44 w-44 items-center justify-center rounded-full border-[14px] border-blue-500 bg-slate-950 shadow-[0_0_35px_rgba(59,130,246,0.25)]">
                <span className="text-5xl font-black text-white">{match.match_score}%</span>
              </div>
              <p className="mt-4 text-sm leading-6 text-slate-400">{match.explanation}</p>
            </>
          ) : (
            <div className="mt-4 rounded-3xl border border-dashed border-slate-800 bg-slate-900/40 p-5 text-sm text-slate-500">
              Paste a job description and run analysis to see match score.
            </div>
          )}
        </div>
      </div>

      {analysis && (
        <>
          <div className="grid gap-4 lg:grid-cols-3">
            <SkillList title="Matched Skills" items={analysis.matched_skills} icon={CheckCircle2} tone="green" />
            <SkillList title="Missing Skills" items={analysis.missing_skills} icon={XCircle} tone="red" />
            <SkillList title="Partial Skills" items={analysis.partial_skills} icon={CircleDashed} tone="amber" />
          </div>

          <div className="rounded-3xl border border-slate-800 bg-slate-950/70 p-5">
            <h2 className="text-lg font-black text-white">Recommended Learning Order</h2>
            <div className="mt-4 flex flex-wrap gap-2">
              {analysis.recommended_learning_order.length === 0 ? (
                <p className="text-sm text-slate-500">No missing skills detected.</p>
              ) : analysis.recommended_learning_order.map((skill, index) => (
                <span key={skill} className="rounded-full bg-slate-900 px-3 py-1.5 text-sm font-black text-slate-300">
                  {index + 1}. {skill}
                </span>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
