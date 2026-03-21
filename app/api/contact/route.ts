import { NextResponse } from 'next/server';
import { z } from 'zod';
import { prisma } from '@/lib/prisma';
const schema = z.object({ name: z.string().min(2), email: z.string().email(), message: z.string().min(10) });
export async function POST(req: Request) { const data = schema.parse(await req.json()); await prisma.contactRequest.create({ data }); return NextResponse.json({ ok: true }); }
