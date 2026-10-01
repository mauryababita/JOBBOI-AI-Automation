import { useEffect, useState } from 'react';
import { Calendar, FileText, RefreshCw, ShieldCheck, Trash2 } from 'lucide-react';
import { deleteResume, listResumes } from '../services/api';

function formatDate(value) {
  if (!value) return 'Unknown date';
  return new Date(value).toLocaleString();
}

export default function ResumeLibraryPage({ token }) {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [deletingId, setDeletingId] = useState(null);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');

  const loadResumes = async () => {
    if (!token) return;
    setLoading(true);
    setError('');
    try {
      const result = await listResumes(token);
      setResumes(result.data.resumes || []);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadResumes();
  }, [token]);

  const handleDelete = async (resume) => {
    const confirmed = window.confirm(`Delete "${resume.file_name}"?`);
    if (!confirmed) return;

    setDeletingId(resume.id);
    setError('');
    setNotice('');
    try {
      await deleteResume({ resumeId: resume.id, token });
      setResumes((current) => current.filter((item) => item.id !== resume.id));
      setNotice('Resume deleted');
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <div className="space-y-6">
      <section className="rounded-3xl border border-slate-800 bg-slate-950/70 p-6">
        <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.2em] text-fuchsia-300">Resume Library</p>
            <h1 className="mt-2 text-3xl font-black text-white">Uploaded Resumes</h1>
            <p className="mt-2 text-sm text-slate-400">Manage uploaded resumes separately from the upload screen.</p>
          </div>
          <button
            type="button"
            onClick={loadResumes}
            disabled={loading}
            className="inline-flex items-center justify-center gap-2 rounded-2xl border border-slate-800 px-4 py-2 text-sm font-black text-slate-200 transition hover:bg-slate-900 disabled:opacity-60"
          >
            <RefreshCw size={16} className={loading ? 'animate-spin' : ''} />
            Refresh
          </button>
        </div>

        {notice && <p className="mt-5 rounded-2xl border border-emerald-500/30 bg-emerald-500/10 p-3 text-sm font-bold text-emerald-200">{notice}</p>}
        {error && <p className="mt-5 rounded-2xl border border-rose-500/30 bg-rose-500/10 p-3 text-sm text-rose-200">{error}</p>}
      </section>

      <section className="space-y-3">
        {resumes.length === 0 ? (
          <div className="rounded-3xl border border-slate-800 bg-slate-950/70 p-10 text-center">
            <FileText className="mx-auto text-slate-500" size={38} />
            <p className="mt-4 text-lg font-black text-white">No resumes uploaded yet</p>
            <p className="mt-2 text-sm text-slate-500">Upload a resume from the Resume page, then manage it here.</p>
          </div>
        ) : resumes.map((resume) => {
          const parsed = resume.parsed_data || {};
          const skills = [
            ...(parsed.technical_skills || []),
            ...(parsed.skills || []),
          ].filter(Boolean).slice(0, 8);

          return (
            <article key={resume.id} className="rounded-3xl border border-slate-800 bg-slate-950/70 p-5">
              <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                <div className="min-w-0">
                  <div className="flex flex-wrap items-center gap-2">
                    <FileText className="text-fuchsia-300" size={20} />
                    <h2 className="truncate text-xl font-black text-white">{resume.file_name}</h2>
                  </div>
                  <p className="mt-2 text-sm text-slate-400">{parsed.name || 'Candidate name not detected'}</p>
                  <div className="mt-3 flex flex-wrap gap-2">
                    <span className="inline-flex items-center gap-2 rounded-full border border-blue-500/30 bg-blue-500/10 px-3 py-1 text-xs font-black text-blue-200">
                      <ShieldCheck size={14} />
                      ATS {resume.ats_score ?? 0}/100
                    </span>
                    <span className="inline-flex items-center gap-2 rounded-full border border-slate-800 bg-slate-900 px-3 py-1 text-xs font-bold text-slate-300">
                      <Calendar size={14} />
                      {formatDate(resume.created_at)}
                    </span>
                  </div>
                  <div className="mt-4 flex flex-wrap gap-2">
                    {skills.length === 0 ? (
                      <span className="rounded-xl bg-slate-900 px-3 py-1.5 text-xs font-bold text-slate-500">No skills detected</span>
                    ) : skills.map((skill) => (
                      <span key={skill} className="rounded-xl bg-slate-900 px-3 py-1.5 text-xs font-bold text-slate-300">{skill}</span>
                    ))}
                  </div>
                </div>

                <button
                  type="button"
                  onClick={() => handleDelete(resume)}
                  disabled={deletingId === resume.id}
                  className="inline-flex items-center justify-center gap-2 rounded-2xl border border-rose-500/30 bg-rose-500/10 px-4 py-2 text-sm font-black text-rose-200 transition hover:bg-rose-500/15 disabled:opacity-60"
                >
                  <Trash2 size={16} />
                  {deletingId === resume.id ? 'Deleting...' : 'Delete'}
                </button>
              </div>
            </article>
          );
        })}
      </section>
    </div>
  );
}
