import { LoginForm } from '@/components/forms/auth-form';
export default function LoginPage() { return <div className="container-page section"><div className="mx-auto max-w-md rounded-2xl bg-white p-8 shadow-soft"><h1 className="text-3xl font-bold">Вход</h1><p className="mt-2 text-slate-600">Войдите, чтобы продолжить обучение.</p><div className="mt-6"><LoginForm /></div></div></div>; }
