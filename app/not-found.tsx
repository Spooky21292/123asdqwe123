import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default function NotFound() {
  return <div className="container-page section text-center"><h1 className="text-4xl font-bold">Страница не найдена</h1><p className="mt-4 text-slate-600">Проверьте адрес или вернитесь на главную.</p><Link href="/" className="mt-6 inline-block"><Button>На главную</Button></Link></div>;
}
