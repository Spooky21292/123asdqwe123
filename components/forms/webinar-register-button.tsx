'use client';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';
export function WebinarRegisterButton({ id }: { id: string }) { return <Button onClick={async()=>{ const res=await fetch(`/api/webinars/${id}/register`,{method:'POST'}); const data=await res.json(); if(!res.ok) return toast.error(data.error||'Ошибка'); toast.success('Вы записаны на вебинар'); }} type="button">Записаться</Button>; }
