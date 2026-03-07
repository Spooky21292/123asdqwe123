import { PropsWithChildren } from 'react';

type GlassCardProps = PropsWithChildren<{
  className?: string;
}>;

export function GlassCard({ className = '', children }: GlassCardProps) {
  return (
    <div
      className={`rounded-2xl border border-white/10 bg-white/[0.04] backdrop-blur-xl shadow-glow ${className}`}
    >
      {children}
    </div>
  );
}
