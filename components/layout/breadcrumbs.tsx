import Link from 'next/link';
export function Breadcrumbs({ items }: { items: { label: string; href?: string }[] }) {
  return <div className="mb-6 flex flex-wrap items-center gap-2 text-sm text-slate-500">{items.map((item, i) => <span key={item.label} className="flex items-center gap-2">{i > 0 && <span>/</span>}{item.href ? <Link href={item.href} className="hover:text-slate-900">{item.label}</Link> : <span className="text-slate-900">{item.label}</span>}</span>)}</div>;
}
