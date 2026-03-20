import NextAuth from 'next-auth';
declare module 'next-auth' {
  interface Session { user: { id: string; name?: string | null; email?: string | null; role?: string; ageGroup?: string } }
  interface User { role?: string; ageGroup?: string }
}
declare module 'next-auth/jwt' { interface JWT { role?: string; ageGroup?: string } }
