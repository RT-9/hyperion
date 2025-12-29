<script lang="ts">
    import "./layout.css";
    import { onMount } from 'svelte';
    import { api } from '$lib/api';
    import SetupWizard from '$lib/components/system/SetupWizard.svelte';
    import LoginModal from '$lib/components/system/LoginModal.svelte';

    /**
     * Root layout for Hyperion.
     * Handles global state, authentication, and the persistent navigation bar.
     * * :param children: The snippet containing the current page content.
     */
    let { children } = $props();

    let isLoading = $state(true);
    let setupNeeded = $state(false);
    let showLogin = $state(false);
    let isLoggedIn = $state(false);
    let user = $state<any>(null);

    /**
     * Executes the system bootstrap process to verify health and session.
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

    onMount(() => {
        bootstrap();
    });

    function onSetupComplete() {
        setupNeeded = false;
        bootstrap();
    }

    function handleLoginSuccess() {
        isLoggedIn = true;
        showLogin = false; // Schliesst das Modal nach Erfolg
        bootstrap();
    }
</script>

{#if isLoading}
    <div class="fixed inset-0 bg-black flex items-center justify-center text-cyan-500 z-[110]">
        <svg class="animate-spin h-8 w-8" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
    </div>
{/if}

{#if showLogin}
    <LoginModal close={() => showLogin = false} onLoginSuccess={handleLoginSuccess} />
{/if}

{#if !isLoading && setupNeeded}
    <SetupWizard onComplete={onSetupComplete} />
{/if}

<div class="min-h-screen bg-slate-950 text-white flex flex-col relative overflow-hidden transition-all duration-700
    {isLoading || setupNeeded || showLogin ? 'blur-xl brightness-50 pointer-events-none h-screen scale-105' : 'blur-0 brightness-100'}">
    
    <div class="absolute top-[-20%] left-[-10%] w-[50vw] h-[50vw] bg-blue-900/10 rounded-full blur-[120px] pointer-events-none"></div>
    <div class="absolute bottom-[-10%] right-[-10%] w-[40vw] h-[40vw] bg-cyan-900/5 rounded-full blur-[100px] pointer-events-none"></div>

    <nav class="relative z-10 px-6 md:px-10 py-6 flex justify-between items-center border-b border-white/5 bg-slate-950/50 backdrop-blur-sm">
        <div class="flex items-center gap-3">
            <div class="text-2xl font-bold tracking-tighter">
                <a href="/">HYPERION<span class="text-cyan-500">.</span></a>
            </div>
            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-orange-500/10 text-orange-400 border border-orange-500/20 uppercase tracking-wide">Pre-Alpha</span>
        </div>

        <div class="flex items-center gap-8">
            <div class="hidden md:flex gap-6 text-xs text-slate-500 font-mono">
                <span class="text-cyan-400 font-bold uppercase tracking-widest text-[10px]">Community Owned</span>
                <span class="flex items-center gap-1"><span class="w-1.5 h-1.5 bg-green-500 rounded-full"></span> GPL3+</span>
            </div>

            {#if !isLoggedIn}
                <button onclick={() => showLogin = true} class="text-[10px] font-black uppercase tracking-widest px-6 py-2 border border-white/10 rounded-full hover:bg-white hover:text-black transition-all">Operator Login</button>
            {:else}
                <div class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-cyan-400 bg-cyan-400/10 px-4 py-2 rounded-full border border-cyan-400/20">
                    <span class="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-pulse"></span> Access Granted: {user?.username}
                </div>
            {/if}
        </div>
    </nav>

    <main class="relative z-10 flex-1 flex flex-col">
        {@render children()}
    </main>
</div>