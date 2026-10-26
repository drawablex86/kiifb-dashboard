<script lang="ts">
	/**
	 * Button.svelte — primitive action button, shadcn-svelte-aligned variant
	 * system (designsystem.md §13.3).
	 *
	 * Variants: primary | secondary | outline | ghost | destructive
	 * Sizes:    sm | md | lg
	 *
	 * Renders <a> when `href` is given (arrow support is a signifier the parent
	 * supplies in markup). Every state change (hover, disabled, focus) is
	 * visually signalled — Norman P4. Disabled also disables pointer events
	 * *and* dims, so the constraint is perceivable (P6).
	 */
	import type { Snippet } from 'svelte';

	type Variant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'destructive';
	type Size = 'sm' | 'md' | 'lg';

	let {
		children,
		variant = 'primary',
		size = 'md',
		href = undefined,
		type = 'button',
		disabled = false,
		class: extra = ''
	}: {
		children: Snippet;
		variant?: Variant;
		size?: Size;
		/** When set, renders as a link styled as this button. */
		href?: string;
		type?: 'button' | 'submit' | 'reset';
		disabled?: boolean;
		/** Extra Tailwind classes merged last (for overrides). */
		class?: string;
	} = $props();

	const variantClass: Record<Variant, string> = {
		primary: 'bg-primary text-primary-foreground shadow-sm hover:bg-primary-hover',
		secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary-hover',
		outline: 'bg-card text-foreground border border-border shadow-sm hover:bg-slate-50',
		ghost: 'text-slate-700 hover:bg-accent hover:text-accent-foreground',
		destructive: 'bg-destructive text-destructive-foreground shadow-sm hover:bg-red-800'
	};

	const sizeClass: Record<Size, string> = {
		sm: 'h-8 px-3 text-xs gap-1.5 rounded-sm',
		md: 'h-9 px-4 text-sm gap-2 rounded-md',
		lg: 'h-10 px-5 text-sm gap-2 rounded-md'
	};

	const base =
		/* Static transparent outline reserves the ring's box (no layout shift);
		   hover paints a soft grey ring (the mouse-user signifier), keyboard focus
		   upgrades it to the global blue focus ring (same box, app.css §9.2). */
		'inline-flex select-none items-center justify-center font-medium transition-all outline-2 outline-offset-2 outline-transparent hover:outline-slate-300 focus-visible:outline-2 focus-visible:outline-ring disabled:pointer-events-none disabled:opacity-50';

	const classes = $derived([base, variantClass[variant], sizeClass[size], extra].join(' '));
</script>

{#if href}
	<a {href} class={classes}>
		{@render children()}
	</a>
{:else}
	<button {type} {disabled} class={classes}>
		{@render children()}
	</button>
{/if}
