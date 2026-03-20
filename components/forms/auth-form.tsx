'use client';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { signIn } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

const registerSchema = z.object({ name: z.string().min(2), email: z.string().email(), password: z.string().min(6), ageGroup: z.enum(['teen','young','adult']) });
const loginSchema = registerSchema.omit({ name: true, ageGroup: true });

export function RegisterForm() {
  const router = useRouter();
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<z.infer<typeof registerSchema>>({ resolver: zodResolver(registerSchema) });
  const onSubmit = async (data: z.infer<typeof registerSchema>) => {
    const res = await fetch('/api/register', { method: 'POST', body: JSON.stringify(data) });
    if (!res.ok) return toast.error('Не удалось создать аккаунт');
    await signIn('credentials', { email: data.email, password: data.password, redirect: false });
    toast.success('Аккаунт создан'); router.push('/dashboard');
  };
  return <form onSubmit={handleSubmit(onSubmit)} className="space-y-4"> <Input placeholder="Имя" {...register('name')} /> <p className="text-xs text-red-500">{errors.name?.message}</p> <Input placeholder="Email" {...register('email')} /> <Input type="password" placeholder="Пароль" {...register('password')} /> <select className="h-11 w-full rounded-xl border border-slate-200 px-3" {...register('ageGroup')}><option value="teen">12–17 лет</option><option value="young">18–30 лет</option><option value="adult">30–45 лет</option></select> <Button disabled={isSubmitting} className="w-full">Зарегистрироваться</Button> </form>;
}

export function LoginForm() {
  const router = useRouter();
  const { register, handleSubmit, formState: { isSubmitting } } = useForm<z.infer<typeof loginSchema>>({ resolver: zodResolver(loginSchema) });
  const onSubmit = async (data: z.infer<typeof loginSchema>) => {
    const res = await signIn('credentials', { ...data, redirect: false });
    if (res?.error) return toast.error('Неверный email или пароль');
    toast.success('Добро пожаловать'); router.push('/dashboard');
  };
  return <form onSubmit={handleSubmit(onSubmit)} className="space-y-4"><Input placeholder="Email" {...register('email')} /><Input type="password" placeholder="Пароль" {...register('password')} /><Button disabled={isSubmitting} className="w-full">Войти</Button></form>;
}
