import { notFound } from 'next/navigation';
import { prisma } from '@/lib/prisma';
import { Breadcrumbs } from '@/components/layout/breadcrumbs';
import { ProgressButton } from '@/components/forms/progress-button';
import { QuizForm } from '@/components/forms/quiz-form';

export default async function LessonPage({ params }: { params: { slug: string; lessonId: string } }) {
  const lesson = await prisma.lesson.findUnique({ where: { id: params.lessonId }, include: { course: true, quiz: { include: { questions: true } } } });
  if (!lesson || lesson.course.slug !== params.slug) notFound();
  return <div className="container-page section"><Breadcrumbs items={[{label:'Курсы',href:'/courses'},{label:lesson.course.title,href:`/courses/${lesson.course.slug}`},{label:lesson.title}]} /><h1 className="text-4xl font-bold">{lesson.title}</h1><p className="mt-3 text-slate-600">{lesson.description}</p><div className="mt-8 aspect-video overflow-hidden rounded-2xl border"><iframe className="h-full w-full" src={lesson.videoUrl} allowFullScreen /></div><article className="prose prose-slate mt-8 max-w-none whitespace-pre-line">{lesson.content}</article><div className="mt-6"><ProgressButton lessonId={lesson.id} /></div>{lesson.quiz && <div className="mt-10"><h2 className="text-2xl font-bold">Тест: {lesson.quiz.title}</h2><div className="mt-6"><QuizForm quiz={lesson.quiz} lessonId={lesson.id} /></div></div>}</div>;
}
