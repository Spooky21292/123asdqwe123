'use client';
import { BarChart, Bar, ResponsiveContainer, XAxis, YAxis, Tooltip } from 'recharts';
export function ProgressChart({ data }: { data: { name: string; progress: number }[] }) { return <ResponsiveContainer width="100%" height="100%"><BarChart data={data}><XAxis dataKey="name" /><YAxis /><Tooltip /><Bar dataKey="progress" fill="#2563eb" radius={[8,8,0,0]} /></BarChart></ResponsiveContainer>; }
