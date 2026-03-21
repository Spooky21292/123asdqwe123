import { notFound } from 'next/navigation';
import { prisma } from '@/lib/prisma';
import { Breadcrumbs } from '@/components/layout/breadcrumbs';
export default async function ArticlePage({ params }: { params: { slug: string } }) { const article = await prisma.article.findUnique({ where: { slug: params.slug } }); if (!article || !article.isPublished) notFound(); return <div className="container-page section"><Breadcrumbs items={[{label:'Блог',href:'/blog'},{label:article.title}]} /><h1 className="text-4xl font-bold">{article.title}</h1><p className="mt-2 text-sm text-slate-500">{article.category}</p><article className="prose prose-slate mt-8 max-w-4xl whitespace-pre-line">{article.content}</article></div>; }
