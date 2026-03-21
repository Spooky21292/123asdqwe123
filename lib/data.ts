import { prisma } from '@/lib/prisma';

export async function getHomepageData() {
  const [courses, webinars, articles, botFeatures] = await Promise.all([
    prisma.course.findMany({ where: { isPublished: true }, take: 3, include: { lessons: true } }),
    prisma.webinar.findMany({ where: { isPublished: true }, orderBy: { date: 'asc' }, take: 3 }),
    prisma.article.findMany({ where: { isPublished: true }, orderBy: { createdAt: 'desc' }, take: 3 }),
    prisma.botFeature.findMany({ take: 4 })
  ]);
  return { courses, webinars, articles, botFeatures };
}
