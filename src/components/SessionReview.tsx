import { motion } from 'framer-motion';
import { CheckCircle2, Flame, MessageCircleMore, ShieldAlert } from 'lucide-react';
import { SessionDraft } from '../types';
import { GlassCard } from './GlassCard';

type SessionReviewProps = {
  draft: SessionDraft;
  completed: boolean;
  distractions: number;
  reflection: string;
  streak: number;
  focusScore: number;
  onChangeReflection: (value: string) => void;
  onSave: () => void;
};

export function SessionReview({
  draft,
  completed,
  distractions,
  reflection,
  streak,
  focusScore,
  onChangeReflection,
  onSave,
}: SessionReviewProps) {
  return (
    <motion.section initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }}>
      <GlassCard className="p-6 sm:p-8 space-y-5">
        <h2 className="text-2xl font-semibold">Session Review</h2>
        <div className="grid sm:grid-cols-2 gap-3 text-sm">
          <div className="rounded-xl border border-white/10 bg-white/5 p-4">
            <p className="text-white/60">Outcome</p>
            <p className="mt-1 font-medium inline-flex items-center gap-2">
              <CheckCircle2 size={16} className={completed ? 'text-mint' : 'text-white/40'} />
              {completed ? 'Completed' : 'Not completed'}
            </p>
          </div>
          <div className="rounded-xl border border-white/10 bg-white/5 p-4">
            <p className="text-white/60">Distractions</p>
            <p className="mt-1 font-medium inline-flex items-center gap-2"><ShieldAlert size={16} />{distractions}</p>
          </div>
          <div className="rounded-xl border border-white/10 bg-white/5 p-4">
            <p className="text-white/60">Focus score</p>
            <p className="mt-1 font-medium">{focusScore}/100</p>
          </div>
          <div className="rounded-xl border border-white/10 bg-white/5 p-4">
            <p className="text-white/60">Streak</p>
            <p className="mt-1 font-medium inline-flex items-center gap-2"><Flame size={16} className="text-mauve" />{streak} days</p>
          </div>
        </div>

        <label className="block space-y-2">
          <span className="text-sm text-white/80 inline-flex items-center gap-2"><MessageCircleMore size={15} />Reflection</span>
          <textarea
            value={reflection}
            onChange={(event) => onChangeReflection(event.target.value)}
            rows={3}
            className="w-full rounded-xl border border-white/10 bg-black/30 px-4 py-3 outline-none focus:border-neon/60"
            placeholder={`How did "${draft.goal}" feel? What to improve next session?`}
          />
        </label>

        <button onClick={onSave} className="w-full rounded-xl py-3 bg-gradient-to-r from-neon to-mint text-ink font-semibold">Save & Open Dashboard</button>
      </GlassCard>
    </motion.section>
  );
}
