export default function Loading() {
  return <div className="container-page section animate-pulse"><div className="h-12 w-1/3 rounded bg-slate-200" /><div className="mt-6 grid gap-4 md:grid-cols-3">{Array.from({ length: 6 }).map((_, i) => <div key={i} className="h-40 rounded-2xl bg-slate-200" />)}</div></div>;
}
