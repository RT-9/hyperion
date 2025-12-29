<script lang="ts">
    import { goto } from '$app/navigation';

    /**
     * Logic for the landing page hero section.
     */
    async function enterApp() {
        // Die Navigation wird hier ausgelöst, der Auth-Status 
        // wird vom Layout bereitgestellt (oder im Backend geprüft).
        await goto('/console');
    }
</script>

<div class="flex-1 flex flex-col items-center justify-center w-full max-w-7xl mx-auto px-6 py-16">
    <div class="text-center mb-20 max-w-4xl">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-slate-800 bg-slate-900/50 text-xs font-mono text-cyan-500 mb-6 uppercase tracking-widest">
            <span class="w-2 h-2 rounded-full bg-cyan-500 animate-pulse"></span> 
            The Modernisation Attempt
        </div>
        
        <h1 class="text-5xl md:text-7xl font-black tracking-tight leading-none mb-8">
            No Dongles. <br /> 
            No Paywalls. <br /> 
            <span class="bg-gradient-to-r from-cyan-400 via-white to-slate-400 bg-clip-text text-transparent">Just Light.</span>
        </h1>
        
        <p class="text-lg text-slate-400 leading-relaxed max-w-2xl mx-auto font-light">
            Hyperion belongs to the community, not a corporation. 
            We are rebuilding DMX control from the ground up to replace outdated industry standards.
        </p>
    </div>

    <div class="flex flex-col md:flex-row items-center gap-6">
        <button 
            onclick={enterApp} 
            class="px-10 py-4 bg-white hover:bg-cyan-50 text-black font-bold rounded-full transition-all hover:scale-105 shadow-[0_0_30px_rgba(255,255,255,0.2)]"
        >
            Ignite Engine
        </button>
        <a href="https://github.com/Arian-Ott/hyperion" target="_blank" class="flex items-center gap-2 px-8 py-4 bg-black border border-slate-800 text-slate-300 rounded-full hover:border-cyan-500 hover:text-white transition-colors">
            Contribute on GitHub
        </a>
    </div>
</div>