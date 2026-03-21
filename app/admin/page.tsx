import { getServerSession } from 'next-auth';
import { redirect } from 'next/navigation';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
import { Card } from '@/components/ui/card';

export default async function AdminPage() {
  const session = await getServerSession(authOptions); if (!session?.user || (session.user as any).role !== 'admin') redirect('/dashboard');
  const [users, courses, contacts, webinars, articles] = await Promise.all([prisma.user.findMany(), prisma.course.findMany({ include: { lessons: true } }), prisma.contactRequest.findMany({ orderBy: { createdAt: 'desc' } }), prisma.webinar.findMany(), prisma.article.findMany()]);
  return <div className="container-page section"><h1 className="text-4xl font-bold">Админ-панель</h1><div className="mt-8 grid gap-6 lg:grid-cols-2"> <Card className="p-6"><h2 className="font-semibold">Пользователи</h2><ul className="mt-4 space-y-2 text-sm">{users.map(u=><li key={u.id}>{u.name} — {u.email} ({u.role})</li>)}</ul></Card> <Card className="p-6"><h2 className="font-semibold">Курсы и уроки</h2><ul className="mt-4 space-y-2 text-sm">{courses.map(c=><li key={c.id}>{c.title} — {c.lessons.length} уроков</li>)}</ul></Card> <Card className="p-6"><h2 className="font-semibold">Вебинары</h2><ul className="mt-4 space-y-2 text-sm">{webinars.map(w=><li key={w.id}>{w.title}</li>)}</ul></Card> <Card className="p-6"><h2 className="font-semibold">Статьи</h2><ul className="mt-4 space-y-2 text-sm">{articles.map(a=><li key={a.id}>{a.title}</li>)}</ul></Card> <Card className="p-6 lg:col-span-2"><h2 className="font-semibold">Заявки</h2><ul className="mt-4 space-y-2 text-sm">{contacts.map(c=><li key={c.id}>{c.name} ({c.email}) — {c.message}</li>)}</ul></Card></div><p className="mt-6 text-sm text-slate-500">CRUD можно расширять через API и Prisma Studio; базовый доступ и просмотр данных уже работают.</p></div>;
}
