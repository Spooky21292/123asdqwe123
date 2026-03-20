import type { Config } from 'tailwindcss';

export default {
  darkMode: ['class'],
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}', './lib/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        border: 'hsl(214 32% 91%)',
        input: 'hsl(214 32% 91%)',
        ring: 'hsl(214 80% 45%)',
        background: 'hsl(210 40% 98%)',
        foreground: 'hsl(222.2 47.4% 11.2%)',
        primary: { DEFAULT: 'hsl(221 83% 53%)', foreground: 'white' },
        secondary: { DEFAULT: 'hsl(162 73% 46%)', foreground: 'white' },
        muted: { DEFAULT: 'hsl(210 40% 96.1%)', foreground: 'hsl(215.4 16.3% 46.9%)' },
        card: { DEFAULT: 'white', foreground: 'hsl(222.2 47.4% 11.2%)' }
      },
      boxShadow: { soft: '0 20px 50px -20px rgba(15, 23, 42, 0.35)' }
    }
  },
  plugins: []
} satisfies Config;
