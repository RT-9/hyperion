<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { api } from '$lib/api';
    import SetupWizard from '$lib/components/system/SetupWizard.svelte';
    import LoginModal from '$lib/components/system/LoginModal.svelte';

    /**
     * Main State Management for the Hyperion Entry Point.
     *
     * :ivar isLoading: Displays a global spinner while synchronising with the backend.
     * :ivar setupNeeded: Determines if the administrative setup wizard should be overlaid.
     * :ivar showLogin: Toggles the authentication interface.
     * :ivar isLoggedIn: Tracks the current session status.
     * :ivar user: Stores the authorised operator's profile data.
     */
    let isLoading = $state(true);
    let setupNeeded = $state(false);
    let showLogin = $state(false);
    let isLoggedIn = $state(false);
    let user = $state<any>(null);

    /**
     * Performs a system health check and session restoration.
     * Hits GET /api/startup/initial-procedure and GET /api/accounts.
     */
    async function bootstrap() {
        try {
            // 1. Check system requirement for setup
            setupNeeded = await api<boolean>('/api/startup/initial-procedure');

            // 2. Attempt to restore an existing session
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
        bootstrap(); // Refresh status after setup
    }

    function handleLoginSuccess() {
        isLoggedIn = true;
        bootstrap(); // Sync user data
    }

    async function enterApp() {
        if (isLoggedIn) {
            await goto('/console');
        } else {
            showLogin = true;
        }
    }
</script>

{#if isLoading}
    <div class="fixed inset-0 bg-black flex items-center justify-center text-cyan-500 z-[100]">
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
                HYPERION<span class="text-cyan-500">.</span>
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
                    <span class="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-pulse"></span> Access Granted
                </div>
            {/if}
        </div>
    </nav>

    <main class="relative z-10 flex-1 flex flex-col items-center w-full max-w-7xl mx-auto px-6 py-16">
        <div class="text-center mb-20 max-w-4xl">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-slate-800 bg-slate-900/50 text-xs font-mono text-cyan-500 mb-6 uppercase tracking-widest">
                <span class="w-2 h-2 rounded-full bg-cyan-500 animate-pulse"></span> The Modernisation Attempt
            </div>
            <h1 class="text-5xl md:text-7xl font-black tracking-tight leading-none mb-8">No Dongles. <br /> No Paywalls. <br /> <span class="bg-gradient-to-r from-cyan-400 via-white to-slate-400 bg-clip-text text-transparent">Just Light.</span></h1>
            <p class="text-lg text-slate-400 leading-relaxed max-w-2xl mx-auto font-light">Hyperion belongs to the community, not a corporation. We are rebuilding DMX control from the ground up to replace outdated industry standards.</p>
        </div>

        <div class="flex flex-col md:flex-row items-center gap-6">
            <button onclick={enterApp} class="px-10 py-4 bg-white hover:bg-cyan-50 text-black font-bold rounded-full transition-all hover:scale-105 shadow-[0_0_30px_rgba(255,255,255,0.2)]">Ignite Engine</button>
            <a href="https://github.com/Arian-Ott/hyperion" target="_blank" class="flex items-center gap-2 px-8 py-4 bg-black border border-slate-800 text-slate-300 rounded-full hover:border-cyan-500 hover:text-white transition-colors">Contribute on GitHub</a>
        </div>
    </main>
</div>

