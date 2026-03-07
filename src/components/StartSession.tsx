import { motion } from 'framer-motion';
import { Sparkles } from 'lucide-react';
import { SessionDraft, SessionType } from '../types';
import { GlassCard } from './GlassCard';

const types: SessionType[] = ['Deep Work', 'Creative Sprint', 'Planning', 'Learning'];
const durations = [25, 45, 60, 90];

type StartSessionProps = {
  draft: SessionDraft;
  setDraft: (value: SessionDraft) => void;
  onStart: () => void;
};

export function StartSession({ draft, setDraft, onStart }: StartSessionProps) {
  const canStart = draft.goal.trim() && draft.task.trim() && draft.why.trim();

  return (
    <motion.section initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }}>
      <GlassCard className="p-5 sm:p-8 space-y-5">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-neon/80">FocusGate Ritual</p>
          <h1 className="text-2xl sm:text-3xl font-semibold mt-2">Start Session</h1>
          <p className="text-sm text-white/60 mt-1">Before the timer starts, define intent. This is your focus gate.</p>
        </div>

        <label className="block space-y-2">
          <span className="text-sm text-white/80">Session Goal</span>
          <input
            value={draft.goal}
            onChange={(event) => setDraft({ ...draft, goal: event.target.value })}
            className="w-full rounded-xl border border-white/10 bg-black/30 px-4 py-3 outline-none focus:border-neon/60"
            placeholder="What outcome will this session create?"
          />
        </label>

        <div className="grid sm:grid-cols-2 gap-4">
          <div className="space-y-2">
            <span className="text-sm text-white/80">Session Type</span>
            <div className="grid grid-cols-2 gap-2">
              {types.map((type) => (
                <button
                  key={type}
                  onClick={() => setDraft({ ...draft, type })}
                  className={`rounded-xl px-3 py-2 text-sm border transition ${draft.type === type ? 'border-neon bg-neon/15' : 'border-white/10 bg-white/5 hover:bg-white/10'}`}
                >
                  {type}
                </button>
              ))}
            </div>
          </div>
          <div className="space-y-2">
            <span className="text-sm text-white/80">Duration</span>
            <div className="grid grid-cols-2 gap-2">
              {durations.map((duration) => (
                <button
                  key={duration}
                  onClick={() => setDraft({ ...draft, duration })}
                  className={`rounded-xl px-3 py-2 text-sm border transition ${draft.duration === duration ? 'border-mint bg-mint/15' : 'border-white/10 bg-white/5 hover:bg-white/10'}`}
                >
                  {duration} min
                </button>
              ))}
            </div>
          </div>
        </div>

        <label className="block space-y-2">
          <span className="text-sm text-white/80">Why this matters</span>
          <textarea
            value={draft.why}
            onChange={(event) => setDraft({ ...draft, why: event.target.value })}
            rows={3}
            className="w-full rounded-xl border border-white/10 bg-black/30 px-4 py-3 outline-none focus:border-mauve/60"
            placeholder="What does successful focus unlock for you today?"
          />
        </label>

        <label className="block space-y-2">
          <span className="text-sm text-white/80">One Main Task</span>
          <input
            value={draft.task}
            onChange={(event) => setDraft({ ...draft, task: event.target.value })}
            className="w-full rounded-xl border border-white/10 bg-black/30 px-4 py-3 outline-none focus:border-neon/60"
            placeholder="Pick the single highest-leverage task"
          />
        </label>

        <button
          onClick={onStart}
          disabled={!canStart}
          className="w-full rounded-2xl px-5 py-4 bg-gradient-to-r from-neon via-mauve to-mint text-ink font-semibold disabled:opacity-45 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          <Sparkles size={18} /> Start Focus
        </button>
      </GlassCard>
    </motion.section>
  );
}
