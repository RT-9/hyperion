<script lang="ts">
    /**
     * Settings page for Hyperion configuration.
     * Uses Svelte 5 runes for state management.
     */
    let deviceName = $state("Hyperion Runner 01");
</script>

<div class="p-8 bg-slate-950 text-white min-h-screen">
    <h1 class="text-3xl font-bold">System Settings</h1>
    <p class="text-slate-400 mt-2">Configure your DMX hardware and network parameters.</p>
    
    <input 
        type="text" 
        bind:value={deviceName} 
        class="mt-4 bg-slate-900 border border-slate-800 p-2 rounded w-full"
    />
</div>