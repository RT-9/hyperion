<script lang="ts">
    /**
     * A vertical slider component tailored for DMX values.
     * * :ivar value: The current value (0-255), two-way bindable.
     * :ivar color: The visual colour of the fader track (Tailwind class).
     */
    let { value = $bindable(0), color = "bg-cyan-500" } = $props();
</script>

<div class="relative h-64 w-8 bg-slate-800 rounded-full overflow-hidden border border-slate-600 shadow-inner group">
    <div 
        class={`absolute bottom-0 w-full transition-all duration-75 ease-out ${color}`}
        style="height: {(value / 255) * 100}%"
    ></div>

    <input 
        type="range" 
        min="0" 
        max="255" 
        bind:value={value}
        class="absolute inset-0 w-full h-full opacity-0 cursor-pointer appearance-none z-10"
        style="writing-mode: bt-lr; -webkit-appearance: slider-vertical;"
    />
    
    <div class="absolute top-2 w-full text-center text-[10px] text-white opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none font-mono">
        {value}
    </div>
</div>