<script lang="ts">


    function enterApp() {
        alert("Initializing Core System...");

    }
</script>

<div class="min-h-screen bg-slate-950 text-white flex flex-col relative overflow-hidden selection:bg-cyan-500 selection:text-black font-sans">
    
    <div class="absolute top-[-20%] left-[-10%] w-[50vw] h-[50vw] bg-blue-900/10 rounded-full blur-[120px] pointer-events-none"></div>
    <div class="absolute bottom-[-10%] right-[-10%] w-[40vw] h-[40vw] bg-cyan-900/5 rounded-full blur-[100px] pointer-events-none"></div>

    <nav class="relative z-10 px-6 md:px-10 py-6 flex justify-between items-center border-b border-white/5 bg-slate-950/50 backdrop-blur-sm">
        <div class="flex items-center gap-3">
            <div class="text-2xl font-bold tracking-tighter">
                HYPERION<span class="text-cyan-500">.</span>
            </div>
            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-orange-500/10 text-orange-400 border border-orange-500/20 uppercase tracking-wide">
                Pre-Alpha
            </span>
        </div>
        <div class="hidden md:flex gap-6 text-xs text-slate-500 font-mono">
            <span class="flex items-center gap-1 text-cyan-400 font-bold">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
                </svg>
                PROUDLY OWNED BY EVERYONE.
            </span>
            <span class="flex items-center gap-1"><span class="w-1.5 h-1.5 bg-green-500 rounded-full"></span> GPL3+</span>
        </div>
    </nav>

    <main class="relative z-10 flex-1 flex flex-col items-center w-full max-w-7xl mx-auto px-6 py-16">
        
        <div class="text-center mb-20 max-w-4xl">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-slate-800 bg-slate-900/50 text-xs font-mono text-cyan-500 mb-6 uppercase tracking-widest">
                <span class="w-2 h-2 rounded-full bg-cyan-500 animate-pulse"></span>
                The Modernisation Attempt
            </div>
            
            <h1 class="text-5xl md:text-7xl font-black tracking-tight leading-none mb-8">
                No Dongles. <br />
                No Paywalls. <br />
                <span class="bg-gradient-to-r from-cyan-400 via-white to-slate-400 bg-clip-text text-transparent">
                    Just Light.
                </span>
            </h1>
            <p class="text-lg text-slate-400 leading-relaxed max-w-2xl mx-auto font-light">
                Hyperion belongs to the community, not a corporation. 
                We are rebuilding DMX control from the ground up to replace outdated, gatekept industry standards.
            </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 w-full mb-20">
            
            <div class="group relative p-6 rounded-2xl bg-slate-900/40 border border-white/5 hover:border-cyan-500/30 transition-all hover:bg-slate-900/60 overflow-hidden flex flex-col">
                <div class="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 text-cyan-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z" />
                    </svg>
                </div>
                <div class="h-10 w-10 bg-cyan-500/10 rounded-lg flex items-center justify-center mb-4 text-cyan-400">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                </div>
                <h3 class="text-white font-bold mb-2 text-xl">Zero Vendor Lock-in</h3>
                <p class="text-sm text-slate-300 leading-relaxed mb-4">
                    We don't sell parameters. <strong class="text-white">All 65,536 universes</strong> (2 Bytes) are unlocked by default. 
                </p>
                <div class="mt-auto pt-4 border-t border-white/10 text-xs text-slate-400 bg-white/5 -mx-6 -mb-6 p-4">
                    <strong class="text-cyan-400 block mb-1">Need more than 65k?</strong>
                    Please open a GitHub issue. We want to celebrate your madness first, then we'll show you the exact line of code to change.
                </div>
            </div>

            <div class="group relative p-6 rounded-2xl bg-slate-900/40 border border-white/5 hover:border-cyan-500/30 transition-all hover:bg-slate-900/60">
                <div class="h-10 w-10 bg-purple-500/10 rounded-lg flex items-center justify-center mb-4 text-purple-400">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
                    </svg>
                </div>
                <h3 class="text-white font-bold mb-2 text-xl">Any Hardware</h3>
                <p class="text-sm text-slate-300 leading-relaxed">
                    Compatible with anything that runs <strong class="text-white">Python & ArtNet</strong>. 
                    From a Raspberry Pi to a high-end Mini PC. 
                </p>
                <div class="mt-4 pt-4 border-t border-white/5 text-[10px] text-slate-500 font-mono">
                    * Tested with ArtNet view on my PC.
                </div>
            </div>

            <div class="group relative p-6 rounded-2xl bg-slate-900/40 border border-white/5 hover:border-cyan-500/30 transition-all hover:bg-slate-900/60">
                <div class="h-10 w-10 bg-green-500/10 rounded-lg flex items-center justify-center mb-4 text-green-400">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                    </svg>
                </div>
                <h3 class="text-white font-bold mb-2 text-xl">Modern Core</h3>
                <p class="text-sm text-slate-300 leading-relaxed">
                    Built on <strong class="text-white">Python 3.14, FastAPI & Redis</strong>.
                    Open API for total integration. GPL3+ licensed to ensure it stays free forever.
                </p>
            </div>

        </div>

        <div class="flex flex-col md:flex-row items-center gap-6">
            <button 
                onclick={enterApp}
                class="px-10 py-4 bg-white hover:bg-cyan-50 text-black font-bold rounded-full transition-all hover:scale-105 shadow-[0_0_30px_rgba(255,255,255,0.2)]"
            >
                Ignite Engine
            </button>

            <a 
                href="https://github.com/Arian-Ott/hyperion" 
                target="_blank"
                class="flex items-center gap-2 px-8 py-4 bg-black border border-slate-800 text-slate-300 rounded-full hover:border-cyan-500 hover:text-white transition-colors"
            >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
                <span>Contribute on GitHub</span>
            </a>
        </div>
        
        <p class="mt-8 text-xs text-slate-600 font-mono text-center max-w-lg">
            Arian-Ott/hyperion • GPL3+ License<br>
            <span class="opacity-50">Use at your own risk. This is pre-alpha software. No warranties provided.</span>
        </p>

    </main>
</div>