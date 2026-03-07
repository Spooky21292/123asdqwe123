import { motion } from 'framer-motion';
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { CalendarCheck2, Flame, ShieldAlert, Trophy } from 'lucide-react';
import { StoredSession } from '../types';
import { GlassCard } from './GlassCard';

type DashboardProps = {
  sessions: StoredSession[];
  streak: number;
  onNewSession: () => void;
};

export function Dashboard({ sessions, streak, onNewSession }: DashboardProps) {
  const weekly = sessions.slice(-7);
  const avgCompletion = Math.round((sessions.filter((entry) => entry.completed).length / sessions.length) * 100);
  const avgDistractions = (sessions.reduce((sum, entry) => sum + entry.distractions, 0) / sessions.length).toFixed(1);

  const chartData = weekly.map((entry, index) => ({
    day: `S${index + 1}`,
    score: entry.focusScore,
  }));

  return (
    <motion.section initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} className="space-y-4">
      <GlassCard className="p-6 sm:p-8 space-y-5">
        <div className="flex items-center justify-between gap-3">
          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-neon/80">Performance Dashboard</p>
            <h2 className="text-2xl font-semibold mt-1">Focus Intelligence</h2>
          </div>
          <button onClick={onNewSession} className="rounded-xl px-4 py-2 text-sm bg-white/10 border border-white/15 hover:bg-white/15">New Session</button>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-sm">
          <Metric icon={<CalendarCheck2 size={15} />} label="Weekly sessions" value={String(weekly.length)} />
          <Metric icon={<Trophy size={15} />} label="Average completion" value={`${avgCompletion}%`} />
          <Metric icon={<ShieldAlert size={15} />} label="Avg distractions" value={avgDistractions} />
          <Metric icon={<Flame size={15} />} label="Streak" value={`${streak} days`} />
        </div>

        <div className="h-64 rounded-2xl border border-white/10 bg-black/20 p-3">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
              <XAxis dataKey="day" stroke="rgba(255,255,255,0.6)" tickLine={false} axisLine={false} />
              <YAxis stroke="rgba(255,255,255,0.6)" tickLine={false} axisLine={false} />
              <Tooltip contentStyle={{ background: '#0E152A', border: '1px solid rgba(255,255,255,0.15)', borderRadius: 12 }} />
              <Bar dataKey="score" fill="url(#paint)" radius={[12, 12, 0, 0]} />
              <defs>
                <linearGradient id="paint" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#83A7FF" />
                  <stop offset="100%" stopColor="#6FF7D6" />
                </linearGradient>
              </defs>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </GlassCard>
    </motion.section>
  );
}

function Metric({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) {
  return (
    <div className="rounded-xl border border-white/10 bg-white/5 p-3">
      <p className="text-white/65 text-xs inline-flex items-center gap-1">{icon}{label}</p>
      <p className="text-lg font-semibold mt-1">{value}</p>
    </div>
  );
}
