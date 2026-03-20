import Link from 'next/link';

export function Footer() {
  return (
    <footer className="border-t border-slate-200 bg-slate-950 text-slate-200">
      <div className="container-page grid gap-8 py-12 md:grid-cols-3">
        <div><h3 className="text-lg font-semibold">FinSkills Pro</h3><p className="mt-3 text-sm text-slate-400">Онлайн-школа финансовой грамотности: курсы, вебинары, тесты и Telegram-ассистент.</p></div>
        <div><h4 className="font-semibold">Навигация</h4><div className="mt-3 flex flex-col gap-2 text-sm text-slate-400"><Link href="/courses">Курсы</Link><Link href="/blog">Блог</Link><Link href="/webinars">Вебинары</Link></div></div>
        <div><h4 className="font-semibold">Контакты</h4><p className="mt-3 text-sm text-slate-400">support@finskills.pro<br/>Москва / Онлайн</p></div>
      </div>
    </footer>
  );
}
