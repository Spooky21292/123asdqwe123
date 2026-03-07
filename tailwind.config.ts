import type { Config } from 'tailwindcss';

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#070B18',
        neon: '#83A7FF',
        mint: '#6FF7D6',
        mauve: '#C9A8FF',
      },
      boxShadow: {
        glow: '0 25px 60px -20px rgba(137, 157, 255, 0.45)',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      backgroundImage: {
        radial:
          'radial-gradient(circle at 20% 10%, rgba(131,167,255,0.16), transparent 35%), radial-gradient(circle at 80% 0%, rgba(111,247,214,0.12), transparent 34%), radial-gradient(circle at 60% 100%, rgba(201,168,255,0.16), transparent 30%)',
      },
    },
  },
  plugins: [],
} satisfies Config;
