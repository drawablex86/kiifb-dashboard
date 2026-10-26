/** @type {import('tailwindcss').Config} */
// UX v2 theming (designsystem.md §13): raw slate palette retained for legacy
// surfaces; new semantic tokens map CSS variables set in src/app.css.
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				slate: {
					50: '#F8FAFC',
					100: '#F1F5F9',
					200: '#E2E8F0',
					300: '#CBD5E1',
					400: '#94A3B8',
					500: '#64748B',
					600: '#475569',
					700: '#334155',
					800: '#1E293B',
					900: '#0F172A'
				},
				background: 'var(--background)',
				foreground: 'var(--foreground)',
				card: {
					DEFAULT: 'var(--card)',
					foreground: 'var(--card-foreground)'
				},
				popover: {
					DEFAULT: 'var(--popover)',
					foreground: 'var(--popover-foreground)'
				},
				primary: {
					DEFAULT: 'var(--primary)',
					foreground: 'var(--primary-foreground)',
					hover: 'var(--primary-hover)'
				},
				secondary: {
					DEFAULT: 'var(--secondary)',
					foreground: 'var(--secondary-foreground)',
					hover: 'var(--secondary-hover)'
				},
				destructive: {
					DEFAULT: 'var(--destructive)',
					foreground: 'var(--destructive-foreground)'
				},
				muted: {
					DEFAULT: 'var(--muted)',
					foreground: 'var(--muted-foreground)'
				},
				accent: {
					DEFAULT: 'var(--accent)',
					foreground: 'var(--accent-foreground)'
				},
				border: 'var(--border)',
				input: 'var(--input)',
				ring: 'var(--ring)'
			},
			borderRadius: {
				sm: 'calc(var(--radius) - 4px)',
				md: 'calc(var(--radius) - 2px)',
				lg: 'var(--radius)'
			},
			fontFamily: {
				sans: ['-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', '"Helvetica Neue"', 'Arial', 'sans-serif'],
				mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'monospace']
			}
		}
	},
	plugins: []
};
