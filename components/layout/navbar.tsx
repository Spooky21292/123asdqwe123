import Link from 'next/link';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { Button } from '@/components/ui/button';

export async function Navbar() {
  const session = await getServerSession(authOptions);
  const nav = [
    ['Курсы', '/courses'], ['Вебинары', '/webinars'], ['Блог', '/blog'], ['Бот', '/bot'], ['Тарифы', '/pricing'], ['Контакты', '/contact']
  ];
  return (
    <header className="sticky top-0 z-40 border-b border-slate-200 bg-white/90 backdrop-blur">
      <div className="container-page flex h-16 items-center justify-between gap-4">
        <Link href="/" className="text-xl font-bold text-slate-900">FinSkills <span className="text-blue-600">Pro</span></Link>
        <nav className="hidden gap-6 md:flex">{nav.map(([label, href]) => <Link key={href} href={href} className="text-sm text-slate-600 hover:text-slate-900">{label}</Link>)}</nav>
        <div className="flex items-center gap-2">
          {session?.user ? <Link href="/dashboard"><Button>Кабинет</Button></Link> : <><Link href="/auth/login"><Button variant="outline">Войти</Button></Link><Link href="/auth/register"><Button>Регистрация</Button></Link></>}
        </div>
      </div>
    </header>
  );
}
