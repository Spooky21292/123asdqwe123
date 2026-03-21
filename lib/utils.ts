import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const ageLabels = { teen: '12–17 лет', young: '18–30 лет', adult: '30–45 лет' } as const;
export const levelLabels = { basic: 'Базовый', intermediate: 'Средний', advanced: 'Продвинутый' } as const;
