import * as React from 'react';
import { cn } from '@/lib/utils';

export function Button({ className, variant = 'default', ...props }: React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'default' | 'outline' | 'secondary' }) {
  return (
    <button
      className={cn('inline-flex items-center justify-center rounded-xl px-4 py-2.5 text-sm font-semibold transition hover:-translate-y-0.5 disabled:opacity-50', variant === 'default' && 'bg-blue-600 text-white hover:bg-blue-700', variant === 'secondary' && 'bg-emerald-500 text-white hover:bg-emerald-600', variant === 'outline' && 'border border-slate-200 bg-white hover:bg-slate-50', className)}
      {...props}
    />
  );
}
