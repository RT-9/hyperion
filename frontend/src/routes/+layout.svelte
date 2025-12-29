<script lang="ts">
    import "./layout.css";
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { api } from '$lib/api';
    import SetupWizard from '$lib/components/system/SetupWizard.svelte';
    import LoginModal from '$lib/components/system/LoginModal.svelte';

    let { children } = $props();

    let isLoading = $state(true);
    let setupNeeded = $state(false);
    let showLogin = $state(false);
    let isLoggedIn = $state(false);
    let user = $state<any>(null);
    
    // State for the profile dropdown toggle
    let isProfileOpen = $state(false);

    /**
     * Initialises the application by checking setup status and existing sessions.
     * * :returns: A promise that resolves when the bootstrap process completes.
     */
    async function bootstrap() {
        try {
            setupNeeded = await api<boolean>('/api/startup/initial-procedure');
            const userData = await api<any>('/api/accounts');
            if (userData) {
                user = userData;
                isLoggedIn = true;
            }
        } catch (e) {
            isLoggedIn = false;
            user = null;
        } finally {
            isLoading = false;
        }
    }

    /**
     * Terminates the current session and redirects to the landing page.
     * * :returns: A promise that resolves after logging out.
     */
    async function logout() {
        try {
            // Optional: If your backend has a dedicated logout endpoint to clear cookies
            // await api('/api/accounts/logout', { method: 'POST' });
            
            // Local cleanup
            isLoggedIn = false;
            user = null;
            isProfileOpen = false;
            await goto('/');
            // Reload ensures all states are fully reset
            location.reload();
        } catch (e) {
            console.error("Logout failed", e);
        }
    }

    onMount(() => {
        bootstrap();
    });
</script>

<style>
@reference "./layout.css";

    /* Globaler Reset, um sicherzugehen, dass nichts im Weg steht */

</style>

<div class="min-h-screen bg-slate-950 text-white flex flex-col relative overflow-hidden transition-all duration-700
    {isLoading || setupNeeded || showLogin ? 'blur-xl brightness-50 pointer-events-none h-screen scale-105' : 'blur-0 brightness-100'}">
    
    <nav class="relative z-[100] px-6 md:px-10 py-4 flex justify-between items-center border-b border-white/5 bg-slate-950/50 backdrop-blur-md">
        <div class="flex items-center gap-3">
            <div class="text-2xl font-bold tracking-tighter">
                <a href="/">HYPERION<span class="text-cyan-500">.</span></a>
            </div>
        </div>

        <div class="flex items-center gap-8">
            {#if !isLoggedIn}
                <button 
                    onclick={() => showLogin = true} 
                    class="text-[10px] font-black uppercase tracking-widest px-6 py-2 border border-white/10 rounded-full hover:bg-white hover:text-black transition-all"
                >
                    Operator Login
                </button>
            {:else}
                <div class="relative">
                    <button 
                        onclick={() => isProfileOpen = !isProfileOpen}
                        class="flex items-center gap-3 group p-1 pr-3 rounded-full border border-white/5 bg-white/5 hover:bg-white/10 transition-all"
                    >
                        <div class="w-8 h-8 rounded-full bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center text-black font-black text-xs uppercase shadow-lg shadow-cyan-500/20">
                            {user?.username?.[0]}
                        </div>
                        <div class="flex flex-col items-start leading-none">
                            <span class="text-[10px] font-bold text-white uppercase tracking-tighter">{user?.username}</span>
                            <span class="text-[8px] text-cyan-500 font-mono uppercase tracking-widest"></span>
                        </div>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-slate-500 group-hover:text-white transition-transform {isProfileOpen ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M19 9l-7 7-7-7" />
                        </svg>
                    </button>

                    {#if isProfileOpen}
                        <div 
                            class="absolute right-0 mt-3 w-48 bg-slate-900 border border-white/10 rounded-xl shadow-2xl overflow-hidden py-2"
                        >
                            <div class="px-4 py-2 border-b border-white/5 mb-2">
                                <p class="text-[9px] font-mono text-slate-500 uppercase">System Identity</p>
                                <p class="text-xs font-bold text-white truncate">{user?.username}</p>
                            </div>

                            <a href="/profile" class="flex items-center gap-3 px-4 py-2 text-xs text-slate-300 hover:bg-white/5 hover:text-cyan-400 transition-colors">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                </svg>
                                Profile
                            </a>
                            <a href="/console" class="flex items-center gap-3 px-4 py-2 text-xs text-slate-300 hover:bg-white/5 hover:text-cyan-400 transition-colors">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                                </svg>
                                Dashboard
                            </a>
                            <a href="/settings" class="flex items-center gap-3 px-4 py-2 text-xs text-slate-300 hover:bg-white/5 hover:text-cyan-400 transition-colors">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                </svg>
                                Settings
                            </a>
                            
                            <div class="mt-2 pt-2 border-t border-white/5">
                                <button 
                                    onclick={logout}
                                    class="w-full flex items-center gap-3 px-4 py-2 text-xs text-red-400 hover:bg-red-500/10 transition-colors"
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                                    </svg>
                                    Logout
                                </button>
                            </div>
                        </div>
                    {/if}
                </div>
            {/if}
        </div>
    </nav>

    <main class="relative z-10 flex-1 flex flex-col">
        {@render children()}
    </main>
</div>