import Link from 'next/link';
import { prisma } from '@/lib/prisma';
import { Card } from '@/components/ui/card';
import { WebinarRegisterButton } from '@/components/forms/webinar-register-button';
export default async function WebinarsPage() { const webinars = await prisma.webinar.findMany({ where: { isPublished: true }, orderBy: { date: 'asc' } }); return <div className="container-page section"><h1 className="text-4xl font-bold">Вебинары</h1><div className="mt-8 grid gap-6 md:grid-cols-2">{webinars.map(w => <Card key={w.id} className="p-6"><p className="text-sm text-blue-600">{new Date(w.date).toLocaleString('ru-RU')}</p><h2 className="mt-2 text-2xl font-semibold">{w.title}</h2><p className="mt-3 text-slate-600">{w.description}</p><p className="mt-3 text-sm text-slate-500">Спикер: {w.speaker}</p><div className="mt-4 flex gap-3"><Link href={`/webinars/${w.id}`} className="text-blue-600">Подробнее</Link><WebinarRegisterButton id={w.id} /></div></Card>)}</div></div>; }
