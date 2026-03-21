import { getServerSession } from 'next-auth';
import { NextResponse } from 'next/server';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
export async function POST(req: Request) { const session = await getServerSession(authOptions); if (!session?.user) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 }); const { quizId, answers } = await req.json(); const quiz = await prisma.quiz.findUnique({ where: { id: quizId }, include: { questions: true } }); if (!quiz) return NextResponse.json({ error: 'Quiz not found' }, { status: 404 }); const correct = quiz.questions.filter(q => answers[q.id] === q.correctAnswer).length; const score = Math.round(correct / quiz.questions.length * 100); await prisma.quizResult.create({ data: { userId: session.user.id, quizId, score } }); const message = score >= 80 ? 'Отлично' : score >= 50 ? 'Хорошо' : 'Нужно повторить'; return NextResponse.json({ score, message }); }
