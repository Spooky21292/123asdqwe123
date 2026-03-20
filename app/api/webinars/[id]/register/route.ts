import { getServerSession } from 'next-auth';
import { NextResponse } from 'next/server';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
export async function POST(_: Request, { params }: { params: { id: string } }) { const session = await getServerSession(authOptions); if (!session?.user) return NextResponse.json({ error: 'Требуется вход' }, { status: 401 }); await prisma.webinarRegistration.upsert({ where: { userId_webinarId: { userId: session.user.id, webinarId: params.id } }, update: {}, create: { userId: session.user.id, webinarId: params.id } }); return NextResponse.json({ ok: true }); }
