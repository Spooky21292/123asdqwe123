import Link from 'next/link';
import { notFound } from 'next/navigation';
import { prisma } from '@/lib/prisma';
import { Breadcrumbs } from '@/components/layout/breadcrumbs';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

export default async function CoursePage({ params }: { params: { slug: string } }) {
  const course = await prisma.course.findUnique({ where: { slug: params.slug }, include: { lessons: { orderBy: { order: 'asc' } } } });
  if (!course || !course.isPublished) notFound();
  return <div className="container-page section"><Breadcrumbs items={[{label:'Главная',href:'/'},{label:'Курсы',href:'/courses'},{label:course.title}]} /><h1 className="text-4xl font-bold">{course.title}</h1><p className="mt-4 max-w-3xl text-lg text-slate-600">{course.description}</p><div className="mt-6"><Link href={`/courses/${course.slug}/lessons/${course.lessons[0]?.id ?? ''}`}><Button>Начать курс</Button></Link></div><div className="mt-10 grid gap-4">{course.lessons.map((lesson)=> <Card key={lesson.id} className="p-5"><div className="flex items-center justify-between gap-4"><div><h3 className="font-semibold">{lesson.order}. {lesson.title}</h3><p className="text-sm text-slate-600">{lesson.description}</p></div><Link href={`/courses/${course.slug}/lessons/${lesson.id}`} className="text-blue-600">Открыть</Link></div></Card>)}</div></div>;
}
