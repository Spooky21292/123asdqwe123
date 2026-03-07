import { motion } from 'framer-motion';
import { Pause, Play, Siren, Target } from 'lucide-react';
import { SessionDraft } from '../types';
import { GlassCard } from './GlassCard';

type FocusModeProps = {
  draft: SessionDraft;
  remaining: number;
  paused: boolean;
  distractions: number;
  onTogglePause: () => void;
  onDistracted: () => void;
  onEnd: (completed: boolean) => void;
};

const formatTime = (secs: number) => `${String(Math.floor(secs / 60)).padStart(2, '0')}:${String(secs % 60).padStart(2, '0')}`;

export function FocusMode({ draft, remaining, paused, distractions, onTogglePause, onDistracted, onEnd }: FocusModeProps) {
  return (
    <motion.section initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} className="space-y-4">
      <GlassCard className="p-8 text-center space-y-6">
        <p className="text-xs tracking-[0.2em] uppercase text-mint/80">Calm Focus Mode</p>
        <div className="text-6xl sm:text-7xl font-semibold tabular-nums tracking-tight">{formatTime(remaining)}</div>
        <div className="space-y-1">
          <p className="text-lg font-medium">{draft.goal}</p>
          <p className="text-white/60 text-sm">{draft.type} · Main task: {draft.task}</p>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <button onClick={onTogglePause} className="rounded-xl border border-white/10 bg-white/5 p-3 flex items-center justify-center gap-2 hover:bg-white/10">
            {paused ? <Play size={16} /> : <Pause size={16} />}
            {paused ? 'Resume' : 'Pause'}
          </button>
          <button onClick={onDistracted} className="rounded-xl border border-white/10 bg-white/5 p-3 flex items-center justify-center gap-2 hover:bg-white/10">
            <Siren size={16} /> I got distracted
          </button>
        </div>

        <div className="flex justify-between text-sm text-white/65">
          <span>Distractions: {distractions}</span>
          <span className="inline-flex items-center gap-1"><Target size={14} /> stay with intent</span>
        </div>
      </GlassCard>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <button onClick={() => onEnd(true)} className="rounded-xl bg-mint/20 border border-mint/40 py-3">Finish Session</button>
        <button onClick={() => onEnd(false)} className="rounded-xl bg-white/5 border border-white/15 py-3">End Early</button>
      </div>
    </motion.section>
  );
}
