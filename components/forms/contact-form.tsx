'use client';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
const schema = z.object({ name: z.string().min(2), email: z.string().email(), message: z.string().min(10) });
export function ContactForm() { const { register, handleSubmit, reset, formState: { isSubmitting } } = useForm<z.infer<typeof schema>>({ resolver: zodResolver(schema) }); const onSubmit = async (data: z.infer<typeof schema>) => { const res = await fetch('/api/contact', { method: 'POST', body: JSON.stringify(data) }); if (!res.ok) return toast.error('Ошибка отправки'); toast.success('Сообщение отправлено'); reset(); }; return <form onSubmit={handleSubmit(onSubmit)} className="space-y-4"><Input placeholder="Ваше имя" {...register('name')} /><Input placeholder="Email" {...register('email')} /><Textarea placeholder="Сообщение" {...register('message')} /><Button disabled={isSubmitting}>Отправить</Button></form>; }
