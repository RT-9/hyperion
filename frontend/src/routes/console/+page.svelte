<script lang="ts">
    import { onMount, untrack } from 'svelte';
    import { browser } from '$app/environment';

    let dmxValues = $state(new Array(24).fill(0));
    let socket: WebSocket | null = null;
    
    // Buffer for the last transmitted state to prevent redundant frames
    let lastSentFrame = ''; 

    function connect() {
        if (!browser) return;
        socket = new WebSocket('ws://127.0.0.1:2468/ws/engine');
        socket.onopen = () => console.log('✅ Engine Link Online');
    }

    onMount(() => {
        connect();
        return () => socket?.close();
    });

    /**
     * Strict change detection logic.
     * This effect only executes when dmxValues is mutated.
     * We then verify if the content has actually changed before sending.
     */
    $effect(() => {
        // 1. Create a non-reactive snapshot of the current state
        const currentSnapshot = $state.snapshot(dmxValues);
        const currentSerialized = JSON.stringify(currentSnapshot);

        // 2. Only proceed if the data differs from the last sent packet
        if (currentSerialized !== lastSentFrame) {
            if (socket && socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify({
                    universe: 0,
                    channels: currentSnapshot
                }));
                
                // 3. Update the buffer
                lastSentFrame = currentSerialized;
                console.log("📡 Change detected: Frame transmitted");
            }
        }
    });
</script>

<style>
    @reference "../layout.css";
    /* Native vertical styling for maximum performance */
    input[type="range"] {
        writing-mode: bt-lr; 
        appearance: slider-vertical;
        width: 40px;
        height: 300px;
        cursor: pointer;
    }
</style>

<div class="p-10 bg-slate-950 min-h-screen text-white">
    <div class="flex gap-4 overflow-x-auto p-6 bg-black/30 rounded-3xl border border-white/5">
        {#each dmxValues as _, i}
            <div class="flex flex-col items-center gap-4">
                <span class="text-[10px] font-mono text-slate-500">CH {i + 1}</span>
                <input 
                    type="range" 
                    min="0" max="255" 
                    bind:value={dmxValues[i]} 
                />
                <span class="text-cyan-500 font-mono font-bold">{dmxValues[i]}</span>
            </div>
        {/each}
    </div>
</div>