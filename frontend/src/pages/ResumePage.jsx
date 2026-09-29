import { useEffect, useMemo, useState } from 'react';
import { BriefcaseBusiness, FileUp, GraduationCap, ShieldCheck, Sparkles } from 'lucide-react';
import { analyzeResume, listResumes, uploadResume } from '../services/api';

function ScoreRing({ score }) {
  const value = Number(score || 0);
  return (
    <div className="flex h-44 w-44 items-center justify-center rounded-full border-[14px] border-blue-500 bg-slate-950 shadow-[0_0_35px_rgba(59,130,246,0.25)]">
      <div className="text-center">
        <p className="text-5xl font-black text-white">{value}</p>
        <p className="text-sm font-semibold text-slate-500">Good</p>
      </div>
    </div>
  );
}

function CategoryBar({ label, score, max }) {
  const pct = Math.min(100, Math.round((score / Math.max(1, max)) * 100));
  const color = pct >= 75 ? 'bg-emerald-400' : pct >= 45 ? 'bg-blue-500' : 'bg-rose-500';
  return (
    <div className="grid grid-cols-[150px_1fr_52px] items-center gap-3 text-sm">
      <span className="truncate font-semibold text-slate-300">{label}</span>
      <div className="h-2 rounded-full bg-slate-800">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-right text-xs font-bold text-slate-400">{score}/{max}</span>
    </div>
  );
}

export default function ResumePage({ token }) {
  const [resumes, setResumes] = useState([]);
  const [selectedResumeId, setSelectedResumeId] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [atsResults, setAtsResults] = useState({});

  const activeResume = resumes.find((resume) => resume.id === selectedResumeId) || resumes[0];
  const parsed = activeResume?.parsed_data || {};
  const skills = useMemo(() => [
    ...(parsed.technical_skills || []),
    ...(parsed.skills || []),
  ].filter(Boolean).slice(0, 12), [parsed]);

  const loadResumes = async () => {
    if (!token) return;
    try {
      const result = await listResumes(token);
      const items = result.data.resumes || [];
      setResumes(items);
      setSelectedResumeId((current) => current || items[0]?.id || null);
    } catch (requestError) {
      setError(requestError.message);
    }
  };

  useEffect(() => {
    loadResumes();
  }, [token]);

  const handleUpload = async (event) => {
    const file = event.target.files?.[0];
    if (!file || !token) return;

    setLoading(true);
    setError('');
    setSelectedFile(file.name);

    try {
      const result = await uploadResume({ file, token });
      const resumeId = result.data.resume.id;
      const analysis = await analyzeResume({ resumeId, token });
      setAtsResults((current) => ({ ...current, [resumeId]: analysis.data }));
      setSelectedResumeId(resumeId);
      await loadResumes();
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
      event.target.value = null;
    }
  };

  const handleSelectResume = async (resumeId) => {
    setSelectedResumeId(resumeId);
    if (!atsResults[resumeId]) {
      try {
        const analysis = await analyzeResume({ resumeId, token });
        setAtsResults((current) => ({ ...current, [resumeId]: analysis.data }));
      } catch (requestError) {
        setError(requestError.message);
      }
    }
  };

  const atsResult = activeResume ? atsResults[activeResume.id] : null;
  const score = atsResult?.score ?? activeResume?.ats_score ?? 0;
  const categories = atsResult?.categories || {};

  const renderList = (title, items, icon) => {
    const Icon = icon;
    return (
      <section className="rounded-3xl border border-slate-800 bg-slate-950/70 p-5">
        <div className="mb-4 flex items-center gap-2">
          <Icon className="text-fuchsia-300" size={18} />
          <h3 className="text-lg font-black text-white">{title}</h3>
        </div>
        {!items?.length ? (
          <p className="text-sm text-slate-500">No {title.toLowerCase()} found in the selected resume.</p>
        ) : (
          <div className="space-y-3">
            {items.map((item, index) => (
              <div key={`${title}-${index}`} className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4 text-sm text-slate-300">
                {typeof item === 'string' ? item : (
                  <div className="space-y-1">
                    {Object.entries(item).map(([key, value]) => (
                      value && (!Array.isArray(value) || value.length > 0) ? (
                        <p key={key}><span className="font-bold capitalize text-slate-100">{key.replaceAll('_', ' ')}:</span> {Array.isArray(value) ? value.join(', ') : value}</p>
                      ) : null
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </section>
    );
  };

  return (
    <div className="space-y-6">
      <div className="grid gap-6 xl:grid-cols-[320px_1fr]">
        <section className="rounded-3xl border border-slate-800 bg-slate-950/70 p-5 shadow-[0_0_40px_rgba(15,23,42,0.35)]">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-fuchsia-300">Upload Resume</p>
          <h1 className="mt-2 text-2xl font-black text-white">Start by uploading your resume PDF</h1>
          <label className="mt-6 flex min-h-48 cursor-pointer flex-col items-center justify-center rounded-3xl border border-dashed border-fuchsia-500/40 bg-fuchsia-500/10 p-6 text-center transition hover:bg-fuchsia-500/15">
            <FileUp className="text-fuchsia-300" size={36} />
            <span className="mt-3 text-sm font-black text-white">{loading ? 'Parsing resume...' : 'Drop or choose PDF'}</span>
            <span className="mt-2 text-xs text-slate-400">PyMuPDF extraction plus validated profile parsing</span>
            <input type="file" accept="application/pdf" className="hidden" onChange={handleUpload} />
          </label>
          {selectedFile && <p className="mt-4 rounded-xl bg-slate-900 p-3 text-sm text-slate-300">Selected: {selectedFile}</p>}
          {error && <p className="mt-4 rounded-xl border border-rose-500/30 bg-rose-500/10 p-3 text-sm text-rose-200">{error}</p>}
          <div className="mt-6">
            <p className="mb-3 text-xs font-black uppercase tracking-[0.18em] text-slate-500">Uploaded Resumes</p>
            <div className="space-y-2">
              {resumes.length === 0 ? (
                <p className="text-sm text-slate-500">No resumes uploaded yet.</p>
              ) : resumes.map((resume) => (
                <button
                  key={resume.id}
                  type="button"
                  onClick={() => handleSelectResume(resume.id)}
                  className={`w-full rounded-2xl border p-3 text-left transition ${
                    activeResume?.id === resume.id
                      ? 'border-fuchsia-500/60 bg-fuchsia-500/15 text-fuchsia-100'
                      : 'border-slate-800 bg-slate-900/70 text-slate-300 hover:border-slate-700'
                  }`}
                >
                  <p className="truncate text-sm font-black">{resume.file_name}</p>
                  <p className="mt-1 text-xs text-slate-500">ATS {resume.ats_score ?? 0}/100</p>
                </button>
              ))}
            </div>
          </div>
        </section>

        <section className="rounded-3xl border border-slate-800 bg-slate-950/70 p-5">
          <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">Candidate Profile</p>
              <h2 className="mt-2 text-3xl font-black text-white">{parsed.name || 'Upload a resume to build your profile'}</h2>
              <p className="mt-2 text-sm text-slate-400">{activeResume?.file_name || 'Contact info, skills, education, projects, and experience will appear here.'}</p>
              <div className="mt-4 grid gap-2 text-sm text-slate-400 md:grid-cols-2">
                <p><span className="font-bold text-slate-200">Email:</span> {parsed.email || 'Not found'}</p>
                <p><span className="font-bold text-slate-200">Phone:</span> {parsed.phone || 'Not found'}</p>
                <p><span className="font-bold text-slate-200">Location:</span> {parsed.location || 'Not found'}</p>
                <p><span className="font-bold text-slate-200">Summary:</span> {parsed.summary || 'Not found'}</p>
              </div>
              <div className="mt-5 flex flex-wrap gap-2">
                {skills.length === 0 ? ['ai', 'computer vision', 'jupyter', 'power bi', 'data science'].map((skill) => (
                  <span key={skill} className="rounded-xl bg-slate-800 px-3 py-1.5 text-xs font-bold text-slate-300">{skill}</span>
                )) : skills.map((skill) => (
                  <span key={skill} className="rounded-xl bg-slate-800 px-3 py-1.5 text-xs font-bold text-slate-300">{skill}</span>
                ))}
              </div>
            </div>
            <div className="rounded-2xl border border-emerald-500/20 bg-emerald-500/10 px-4 py-3 text-sm font-bold text-emerald-200">
              <div className="flex items-center gap-2">
                <ShieldCheck size={16} />
                ATS-style estimate
              </div>
            </div>
          </div>
        </section>
      </div>

      <section className="rounded-3xl border border-slate-800 bg-slate-950/70 p-6">
        <div className="mb-6 flex items-center gap-3">
          <Sparkles className="text-fuchsia-300" size={20} />
          <h2 className="text-xl font-black text-white">ATS Score & Recommendations</h2>
        </div>
        <div className="grid gap-8 lg:grid-cols-[260px_1fr]">
          <div className="flex justify-center">
            <ScoreRing score={score} />
          </div>
          <div className="space-y-4">
            {Object.keys(categories).length === 0 ? (
              [
                ['Contact Info', 8, 10],
                ['Section Headers', 9, 10],
                ['Skill Keywords', 13, 25],
                ['Action Verbs', 8, 10],
                ['Quantified Impact', 6, 15],
                ['Formatting', 9, 10],
                ['Length', 5, 5],
              ].map(([label, itemScore, max]) => <CategoryBar key={label} label={label} score={itemScore} max={max} />)
            ) : Object.entries(categories).map(([label, value]) => (
              <CategoryBar key={label} label={label} score={value.score} max={value.max} />
            ))}
          </div>
        </div>
        <div className="mt-8 grid gap-6 lg:grid-cols-2">
          <div>
            <p className="mb-3 text-xs font-black uppercase tracking-[0.18em] text-emerald-300">Strengths</p>
            <div className="space-y-3 text-sm text-slate-300">
              {(atsResult?.strengths?.length ? atsResult.strengths : ['Core profile sections are ready once resume is uploaded.', 'Skills can be matched against job descriptions.']).map((item) => (
                <p key={item} className="rounded-2xl border border-slate-800 bg-slate-900/70 p-3">{item}</p>
              ))}
            </div>
          </div>
          <div>
            <p className="mb-3 text-xs font-black uppercase tracking-[0.18em] text-amber-300">Recommendations</p>
            <div className="space-y-3 text-sm text-slate-300">
              {(atsResult?.recommendations?.length ? atsResult.recommendations : ['Add measurable outcomes with numbers, percentages, users, revenue, or scale.', 'Use text-based PDF content for best parsing reliability.']).map((item) => (
                <p key={item} className="rounded-2xl border border-slate-800 bg-slate-900/70 p-3">{item}</p>
              ))}
            </div>
          </div>
        </div>
      </section>

      <div className="grid gap-6 xl:grid-cols-2">
        {renderList('Experience', parsed.experience || [], BriefcaseBusiness)}
        {renderList('Education', parsed.education || [], GraduationCap)}
        {renderList('Projects', parsed.projects || [], Sparkles)}
        {renderList('Certifications', parsed.certifications || [], ShieldCheck)}
        {renderList('Achievements', parsed.achievements || [], Sparkles)}
      </div>
    </div>
  );
}
