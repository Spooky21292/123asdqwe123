import { useEffect, useMemo, useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { Dashboard } from './components/Dashboard';
import { FocusMode } from './components/FocusMode';
import { SessionReview } from './components/SessionReview';
import { StartSession } from './components/StartSession';
import { seedSessions } from './data/mockData';
import { SessionDraft, StoredSession } from './types';

type View = 'start' | 'focus' | 'review' | 'dashboard';

const defaultDraft: SessionDraft = {
  goal: '',
  type: 'Deep Work',
  duration: 45,
  why: '',
  task: '',
};

export default function App() {
  const [view, setView] = useState<View>('start');
  const [draft, setDraft] = useState<SessionDraft>(defaultDraft);
  const [remaining, setRemaining] = useState(defaultDraft.duration * 60);
  const [paused, setPaused] = useState(false);
  const [distractions, setDistractions] = useState(0);
  const [completed, setCompleted] = useState(false);
  const [reflection, setReflection] = useState('');
  const [sessions, setSessions] = useState<StoredSession[]>(seedSessions);

  const streak = useMemo(() => {
    let run = 0;
    for (let index = sessions.length - 1; index >= 0; index -= 1) {
      if (!sessions[index].completed) break;
      run += 1;
    }
    return run;
  }, [sessions]);

  useEffect(() => {
    if (view !== 'focus' || paused || remaining === 0) return;
    const timer = window.setInterval(() => {
      setRemaining((prev) => Math.max(prev - 1, 0));
    }, 1000);
    return () => window.clearInterval(timer);
  }, [view, paused, remaining]);

  useEffect(() => {
    if (view === 'focus' && remaining === 0) {
      handleEnd(true);
    }
  }, [remaining, view]);

  const startFocus = () => {
    setRemaining(draft.duration * 60);
    setDistractions(0);
    setPaused(false);
    setReflection('');
    setView('focus');
  };

  const handleEnd = (isCompleted: boolean) => {
    setCompleted(isCompleted);
    setPaused(true);
    setView('review');
  };

  const saveReview = () => {
    const focusScore = Math.max(30, Math.min(99, Math.round((completed ? 70 : 45) + (draft.duration * 0.2 - distractions * 8))));
    const record: StoredSession = {
      ...draft,
      completed,
      distractions,
      reflection,
      focusScore,
      timestamp: new Date().toISOString(),
    };
    setSessions((prev) => [...prev, record]);
    setView('dashboard');
  };

  const resetSession = () => {
    setDraft(defaultDraft);
    setRemaining(defaultDraft.duration * 60);
    setDistractions(0);
    setReflection('');
    setView('start');
  };

  const previewScore = Math.max(30, Math.min(99, Math.round((completed ? 70 : 45) + (draft.duration * 0.2 - distractions * 8))));

  return (
    <main className="min-h-screen bg-ink bg-radial text-white py-6 px-4 sm:px-6">
      <div className="max-w-3xl mx-auto">
        <AnimatePresence mode="wait">
          {view === 'start' && <StartSession draft={draft} setDraft={setDraft} onStart={startFocus} />}
          {view === 'focus' && (
            <FocusMode
              draft={draft}
              remaining={remaining}
              paused={paused}
              distractions={distractions}
              onTogglePause={() => setPaused((prev) => !prev)}
              onDistracted={() => setDistractions((prev) => prev + 1)}
              onEnd={handleEnd}
            />
          )}
          {view === 'review' && (
            <SessionReview
              draft={draft}
              completed={completed}
              distractions={distractions}
              reflection={reflection}
              focusScore={previewScore}
              streak={streak + (completed ? 1 : 0)}
              onChangeReflection={setReflection}
              onSave={saveReview}
            />
          )}
          {view === 'dashboard' && <Dashboard sessions={sessions} streak={streak} onNewSession={resetSession} />}
        </AnimatePresence>
      </div>
    </main>
  );
}
