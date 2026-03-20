import { getServerSession } from 'next-auth';
import { redirect } from 'next/navigation';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
import { Card } from '@/components/ui/card';
import { ProgressChart } from '@/components/progress-chart';

export default async function DashboardPage() {
  const session = await getServerSession(authOptions); if (!session?.user) redirect('/auth/login');
  const [courses, progress, results, webinars] = await Promise.all([
    prisma.course.findMany({ where: { isPublished: true }, include: { lessons: true } }),
    prisma.userProgress.findMany({ where: { userId: session.user.id, completed: true }, include: { lesson: { include: { course: true } } } }),
    prisma.quizResult.findMany({ where: { userId: session.user.id }, orderBy: { createdAt: 'desc' }, take: 5, include: { quiz: { include: { lesson: true } } } }),
    prisma.webinar.findMany({ where: { isPublished: true, date: { gte: new Date() } }, take: 3, orderBy: { date: 'asc' } })
  ]);
  const totalLessons = courses.reduce((acc,c)=>acc+c.lessons.length,0); const progressPercent = totalLessons ? Math.round(progress.length/totalLessons*100) : 0;
  const chart = courses.map(c => ({ name: c.title.split(' ')[0], progress: c.lessons.length ? Math.round(progress.filter(p=>p.lesson.courseId===c.id).length / c.lessons.length * 100) : 0 }));
  return <div className="container-page section"><h1 className="text-4xl font-bold">Здравствуйте, {session.user.name}</h1><p className="mt-3 text-slate-600">Ваш общий прогресс: {progressPercent}%</p><div className="mt-8 grid gap-6 lg:grid-cols-3"><Card className="p-6 lg:col-span-2"><h2 className="text-xl font-semibold">Прогресс по курсам</h2><div className="mt-6 h-72"><ProgressChart data={chart} /></div></Card><Card className="p-6"><h2 className="text-xl font-semibold">Рекомендации</h2><ul className="mt-4 space-y-3 text-sm text-slate-600"><li>Завершите ближайший урок из начатого курса.</li><li>Пройдите тест, чтобы закрепить материал.</li><li>Запишитесь на ближайший вебинар.</li></ul></Card></div><div className="mt-8 grid gap-6 md:grid-cols-2 lg:grid-cols-3"><Card className="p-6"><h2 className="font-semibold">Начатые курсы</h2><ul className="mt-4 space-y-2 text-sm text-slate-600">{courses.map(c=><li key={c.id}>{c.title}</li>)}</ul></Card><Card className="p-6"><h2 className="font-semibold">Последние результаты тестов</h2><ul className="mt-4 space-y-2 text-sm text-slate-600">{results.length? results.map(r=><li key={r.id}>{r.quiz.lesson.title}: {r.score}%</li>):<li>Пока нет результатов.</li>}</ul></Card><Card className="p-6"><h2 className="font-semibold">Ближайшие вебинары</h2><ul className="mt-4 space-y-2 text-sm text-slate-600">{webinars.map(w=><li key={w.id}>{w.title} — {new Date(w.date).toLocaleDateString('ru-RU')}</li>)}</ul></Card></div></div>;
}
