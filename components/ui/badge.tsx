export function Badge({ children }: { children: React.ReactNode }) {
  return <span className="inline-flex rounded-full bg-blue-50 px-3 py-1 text-xs font-medium text-blue-700">{children}</span>;
}
