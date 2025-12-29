<script lang="ts">
	import { fade, fly } from 'svelte/transition';

	/**
	 * Component for user authentication.
	 *
	 * :param onLoginSuccess: Callback function after successful authentication.
	 * :param close: Function to close the modal.
	 */
	let { onLoginSuccess, close } = $props();

	let username = $state('');
	let password = $state('');
	let loading = $state(false);
	let errorMsg = $state<string | null>(null);

	/**
	 * Submits the login credentials as FormData.
	 * * Since the backend uses a cookie-based APIKeyCookie scheme, 
	 * the browser will automatically handle the 'access_token' cookie.
	 */
	async function handleLogin(e: Event) {
		e.preventDefault();
		loading = true;
		errorMsg = null;

		const formData = new FormData();
		formData.append('username', username);
		formData.append('password', password);

		try {
			const response = await fetch('http://localhost:2468/api/accounts/login', {
				method: 'POST',
                credentials: "include",
				body: formData
			});

			if (!response.ok) throw new Error('Invalid credentials');

			onLoginSuccess();
			close();
		} catch (err: any) {
			errorMsg = err.message;
		} finally {
			loading = false;
		}
	}
</script>

<div class="fixed inset-0 z-[110] flex items-center justify-center p-4 bg-black/40 backdrop-blur-md" transition:fade>
	<div 
		class="w-full max-w-sm bg-slate-900 border border-white/10 rounded-2xl shadow-2xl overflow-hidden"
		transition:fly={{ y: 10, duration: 400 }}
	>
		<div class="h-1 bg-cyan-500"></div>
		
		<div class="p-8">
			<h2 class="text-xl font-bold text-white mb-6 uppercase tracking-tight">Login</h2>

			{#if errorMsg}
				<div class="mb-4 p-3 bg-red-500/10 border border-red-500/50 text-red-400 text-xs rounded">
					{errorMsg}
				</div>
			{/if}

			<form onsubmit={handleLogin} class="space-y-4">
				<div class="space-y-1">
					<label class="text-[10px] font-mono text-slate-500 uppercase" >Identity</label>
					<input
                        id="iserma,e"
						type="text" 
						bind:value={username} 
						required
						placeholder="Username"
						class="w-full bg-black border border-slate-800 rounded-lg p-3 text-white focus:border-cyan-500 outline-none transition-all"
					/>
				</div>
				<div class="space-y-1">
					<label class="text-[10px] font-mono text-slate-500 uppercase">Password</label>
					<input 
						type="password" 
						bind:value={password} 
						required
						placeholder="••••••••"
						class="w-full bg-black border border-slate-800 rounded-lg p-3 text-white focus:border-cyan-500 outline-none transition-all"
					/>
				</div>

				<div class="flex gap-3 pt-4">
					<button 
						type="button" 
						onclick={close}
						class="flex-1 py-3 text-xs font-bold text-slate-400 hover:text-white transition-colors"
					>
						Cancel
					</button>
					<button 
						type="submit" 
						disabled={loading}
						class="flex-[2] py-3 bg-cyan-600 hover:bg-cyan-500 text-black font-black rounded-lg transition-all disabled:opacity-50"
					>
						{loading ? 'Verifying...' : 'Authenticate'}
					</button>
				</div>
			</form>
		</div>
	</div>
</div>