<script lang="ts">
	import '../app.css';
	let { children } = $props();
</script>

<div class="min-h-screen flex flex-col bg-slate-50 text-slate-900">
	<!-- Civic Tech Header -->
	<header class="border-b border-slate-200 bg-white sticky top-0 z-30">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex items-center justify-between">
			<div class="flex items-center space-x-3">
				<div class="w-8 h-8 rounded bg-slate-900 text-white flex items-center justify-center font-bold text-sm tracking-wider">
					KL
				</div>
				<div>
					<h1 class="text-base font-semibold leading-tight text-slate-900">
						KIIFB Accountability & Public Value Dashboard
					</h1>
					<p class="text-xs text-slate-500">
						Source-linked investigation of the 2026 Expert Committee Report vs. documented delivery
					</p>
				</div>
			</div>
			<nav class="flex items-center space-x-1 sm:space-x-3 text-xs sm:text-sm font-medium">
				<a href="/" class="px-3 py-1.5 rounded text-slate-700 hover:text-slate-900 hover:bg-slate-100 transition">
					Assertions
				</a>
				<span class="text-slate-300">|</span>
				<a href="/projects" class="px-3 py-1.5 rounded text-slate-700 hover:text-slate-900 hover:bg-slate-100 transition">
					Project Explorer
				</a>
				<span class="text-slate-300">|</span>
				<span class="px-2 py-1 text-slate-400 cursor-not-allowed" title="Coming in Milestone 3">
					Financials (M3)
				</span>
			</nav>
		</div>
	</header>

	<!-- Main Content Area -->
	<main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
		{@render children()}
	</main>

	<!-- Standard Civic Footer -->
	<footer class="border-t border-slate-200 bg-white py-6 mt-12 text-xs text-slate-500">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row justify-between items-center gap-4">
			<div>
				<span>Public-interest evidence tool. Every displayed assertion is cross-linked to primary source records.</span>
			</div>
			<div class="flex items-center space-x-4">
				<span>Evidence Standard: Strict Provenance</span>
				<span>Oct 2026 Baseline</span>
			</div>
		</div>
	</footer>
</div>
