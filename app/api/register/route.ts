import { NextResponse } from 'next/server';
import bcrypt from 'bcryptjs';
import { z } from 'zod';
import { prisma } from '@/lib/prisma';
const schema = z.object({ name: z.string().min(2), email: z.string().email(), password: z.string().min(6), ageGroup: z.enum(['teen','young','adult']) });
export async function POST(req: Request) { const data = schema.parse(await req.json()); const exists = await prisma.user.findUnique({ where: { email: data.email } }); if (exists) return NextResponse.json({ error: 'Email занят' }, { status: 400 }); const passwordHash = await bcrypt.hash(data.password, 10); await prisma.user.create({ data: { name: data.name, email: data.email, passwordHash, ageGroup: data.ageGroup } }); return NextResponse.json({ ok: true }); }
