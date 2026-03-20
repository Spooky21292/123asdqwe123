# FinSkills Pro

Полноценный MVP full-stack платформы по финансовой грамотности на Next.js 14, TypeScript, Tailwind CSS, Prisma и NextAuth.

## Стек
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Prisma ORM
- SQLite по умолчанию (легко переключить на PostgreSQL через `.env` и `schema.prisma`)
- NextAuth Credentials
- React Hook Form + Zod
- Recharts
- bcryptjs

## Возможности
- Главная страница, каталог курсов, уроки и квизы
- Регистрация, вход и защищённый личный кабинет
- Вебинары и запись на них
- Блог и контакты
- Простая админ-панель для роли `admin`
- Seed-данные для локальной демонстрации

## Быстрый старт
```bash
cp .env.example .env
npm install
npm run db:generate
npm run db:push
npm run db:seed
npm run dev
```

## Переменные окружения
```env
DATABASE_PROVIDER="sqlite"
DATABASE_URL="file:./dev.db"
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="change-me-super-secret"
```

## Миграции / БД
- `npm run db:generate` — генерация Prisma Client
- `npm run db:push` — синхронизация схемы
- `npm run db:migrate` — создание миграции
- `npm run db:seed` — заполнение демо-данными

## Демо-аккаунты
- Админ: `admin@finskills.pro` / `password123`
- Пользователь: `anya@example.com` / `password123`

## Структура
- `app` — страницы, layout, API routes
- `components` — UI, layout и формы
- `lib` — auth, Prisma, утилиты
- `prisma` — schema + seed
- `types` — типы расширения NextAuth

## Переход на PostgreSQL
1. Укажите `DATABASE_PROVIDER="postgresql"`
2. Замените `DATABASE_URL` на PostgreSQL connection string
3. Выполните `npm run db:generate && npm run db:push`
