# FinSkills Pro

Полноценный MVP full-stack платформы по финансовой грамотности на Next.js 14, TypeScript, Tailwind CSS, Prisma и NextAuth, подготовленный для локального запуска и деплоя на Railway.

## Стек
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Prisma ORM
- PostgreSQL
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
- Конфигурация для Railway deploy

## Быстрый старт локально
```bash
cp .env.example .env
npm install
npm run db:generate
npm run db:push
npm run seed
npm run dev
```

## Переменные окружения
```env
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/finskills_pro?schema=public"
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="change-me-super-secret"
```

## Скрипты
- `npm run dev` — локальная разработка
- `npm run build` — production build Next.js + Prisma Client
- `npm start` — запуск production сервера
- `npm run db:generate` — генерация Prisma Client
- `npm run db:push` — синхронизация схемы в БД
- `npm run db:migrate` — локальная миграция Prisma
- `npm run db:deploy` — применение миграций в production, если вы заранее создали их локально
- `npm run seed` / `npm run db:seed` — заполнение демо-данными

## Демо-аккаунты
- Админ: `admin@finskills.pro` / `password123`
- Пользователь: `anya@example.com` / `password123`

## Railway deploy
1. Загрузите проект в GitHub.
2. В Railway создайте `New Project` → `Deploy from GitHub repo`.
3. Добавьте сервис `PostgreSQL` внутри проекта Railway.
4. В web-service откройте `Variables` и укажите:
   - `DATABASE_URL=${{Postgres.DATABASE_URL}}`
   - `NEXTAUTH_SECRET=<длинная случайная строка>`
   - `NEXTAUTH_URL=https://<ваш-домен>.up.railway.app`
5. Railway соберёт приложение через `npm run build` и запустит через `npm start`.
6. Для первого деплоя без подготовленных миграций выполните инициализацию схемы и сид:
   ```bash
   npm run db:push
   npm run seed
   ```
7. Если позже вы начнёте хранить Prisma migrations в репозитории, в production можно перейти на:
   ```bash
   npm run db:deploy
   ```

## Почему PostgreSQL, а не SQLite
Railway использует временную файловую систему для сервисов, поэтому локальный `dev.db` не подходит для production-сценария с авторизацией и постоянными пользовательскими данными. PostgreSQL — рекомендуемый вариант для Railway и Prisma.

## Структура
- `app` — страницы, layout, API routes
- `components` — UI, layout и формы
- `lib` — auth, Prisma, утилиты
- `prisma` — schema + seed
- `types` — типы расширения NextAuth
- `railway.json` — базовая deploy-конфигурация Railway
