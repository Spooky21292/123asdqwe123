'use client';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';
export function ProgressButton({ lessonId }: { lessonId: string }) { return <Button type="button" onClick={async()=>{ const res=await fetch('/api/progress',{method:'POST',body:JSON.stringify({lessonId})}); if(!res.ok) return toast.error('Нужно войти в аккаунт'); toast.success('Урок отмечен как пройденный'); }}>Отметить как пройдено</Button>; }
