import type { Metadata } from 'next';
import './globals.css';
import { Navbar } from '@/components/layout/navbar';
import { Footer } from '@/components/layout/footer';
import { AppToaster } from '@/components/ui/toaster';

export const metadata: Metadata = {
  title: { default: 'FinSkills Pro', template: '%s | FinSkills Pro' },
  description: 'Современная онлайн-платформа по финансовой грамотности для подростков, молодых людей и взрослых.',
  openGraph: { title: 'FinSkills Pro', description: 'Курсы, вебинары, тесты и финансовый ассистент.', type: 'website' }
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ru">
      <body>
        <Navbar />
        <main>{children}</main>
        <Footer />
        <AppToaster />
      </body>
    </html>
  );
}
