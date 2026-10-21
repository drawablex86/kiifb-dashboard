import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	// Fixed, project-specific ports so multiple local projects never clash
	// on Vite's default 5173 (dev) / 4173 (preview).
	server: {
		port: 5174,
		strictPort: true,
		fs: {
			allow: ['src', '.svelte-kit', 'data', 'node_modules']
		}
	},
	preview: {
		port: 4174,
		strictPort: true
	}
});
