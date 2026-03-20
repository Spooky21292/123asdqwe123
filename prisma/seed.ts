import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcryptjs';
const prisma = new PrismaClient();
async function main() {
  await prisma.quizResult.deleteMany(); await prisma.userProgress.deleteMany(); await prisma.quizQuestion.deleteMany(); await prisma.quiz.deleteMany(); await prisma.lesson.deleteMany(); await prisma.course.deleteMany(); await prisma.webinarRegistration.deleteMany(); await prisma.webinar.deleteMany(); await prisma.article.deleteMany(); await prisma.botFeature.deleteMany(); await prisma.contactRequest.deleteMany(); await prisma.user.deleteMany();
  const passwordHash = await bcrypt.hash('password123', 10);
  await prisma.user.createMany({ data: [
    { name: 'Admin Demo', email: 'admin@finskills.pro', passwordHash, ageGroup: 'adult', role: 'admin' },
    { name: 'Аня', email: 'anya@example.com', passwordHash, ageGroup: 'teen', role: 'user' },
    { name: 'Илья', email: 'ilya@example.com', passwordHash, ageGroup: 'young', role: 'user' },
    { name: 'Мария', email: 'maria@example.com', passwordHash, ageGroup: 'adult', role: 'user' }
  ]});
  const courseData = [
    ['Как работают деньги','kak-rabotayut-dengi','teen','basic'],
    ['Первая зарплата и личный бюджет','pervaya-zarplata-i-byudzhet','young','intermediate'],
    ['Защита сбережений от инфляции','zashita-sberezheniy-ot-inflyacii','adult','intermediate']
  ] as const;
  for (const [title, slug, ageGroup, level] of courseData) {
    const course = await prisma.course.create({ data: { title, slug, description: `${title} — практический курс по финансовой грамотности.`, ageGroup, level, coverImage: '/cover.jpg', isPublished: true } });
    for (let i=1;i<=4;i++) {
      const lesson = await prisma.lesson.create({ data: { courseId: course.id, title: `Урок ${i}: ${title}`, description: `Ключевые навыки модуля ${i}.`, videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ', content: `Подробный текст урока ${i} для курса «${title}».

Вы узнаете о бюджете, целях, рисках, инфляции и принятии решений.`, order: i, durationMinutes: 15 + i * 5 } });
      const quiz = await prisma.quiz.create({ data: { lessonId: lesson.id, title: `Проверка по уроку ${i}` } });
      await prisma.quizQuestion.createMany({ data: [1,2,3].map((n)=>({ quizId: quiz.id, question: `Вопрос ${n} по теме урока ${i}?`, optionA: 'Вариант A', optionB: 'Вариант B', optionC: 'Вариант C', optionD: 'Вариант D', correctAnswer: 'A' })) });
    }
  }
  await prisma.webinar.createMany({ data: [
    { title: 'Как говорить с подростками о деньгах', description: 'Семейные сценарии и полезные привычки.', speaker: 'Екатерина Смирнова', date: new Date('2026-04-10T16:00:00Z'), meetingUrl: 'https://example.com/webinar-1', isPublished: true },
    { title: 'Личный бюджет без стресса', description: 'Практика и шаблоны.', speaker: 'Иван Кузнецов', date: new Date('2026-04-15T17:00:00Z'), meetingUrl: 'https://example.com/webinar-2', isPublished: true },
    { title: 'Как понимать инфляцию и ставки', description: 'Образовательный обзор макроэкономики.', speaker: 'Анна Белова', date: new Date('2026-04-20T18:00:00Z'), meetingUrl: 'https://example.com/webinar-3', isPublished: true }
  ]});
  await prisma.botFeature.createMany({ data: [
    { title: 'Напоминания', description: 'Помогает не выпадать из обучения.', icon: 'Bell' },
    { title: 'Ответы на вопросы', description: 'Объясняет термины простым языком.', icon: 'MessageCircle' },
    { title: 'Краткие сводки', description: 'Делает обзор рыночных событий в учебном формате.', icon: 'Newspaper' },
    { title: 'Финансовые привычки', description: 'Подсказывает небольшие шаги на каждый день.', icon: 'Target' }
  ]});
  await prisma.article.createMany({ data: [
    { title: 'Что такое бюджет семьи', slug: 'chto-takoe-byudzhet-semi', excerpt: 'С чего начать планирование расходов.', content: 'Статья о бюджете семьи...', category: 'бюджет', isPublished: true },
    { title: 'Как инфляция влияет на накопления', slug: 'kak-inflyaciya-vliyaet-na-nakopleniya', excerpt: 'Понятно о росте цен и покупательной способности.', content: 'Статья об инфляции...', category: 'инфляция', isPublished: true },
    { title: 'Налоги простыми словами', slug: 'nalogi-prostymi-slovami', excerpt: 'Основы налоговой грамотности.', content: 'Статья о налогах...', category: 'налоги', isPublished: true },
    { title: 'Инвестиции без мифов', slug: 'investicii-bez-mifov', excerpt: 'Обучающий взгляд на риски и горизонты.', content: 'Статья об инвестициях...', category: 'инвестиции', isPublished: true },
    { title: 'Финансовые привычки на каждый день', slug: 'finansovye-privychki-na-kazhdyy-den', excerpt: 'Маленькие шаги к устойчивому поведению.', content: 'Статья о привычках...', category: 'финансовые привычки', isPublished: true }
  ]});
}
main().finally(async()=>{ await prisma.$disconnect(); });
