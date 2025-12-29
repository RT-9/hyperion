<script lang="ts">
	import { Slider } from "bits-ui";
	import { browser } from "$app/environment";

	// Svelte 5: Array von Arrays, da Slider.Root immer ein Array für 'value' braucht
	let dmxValues = $state(new Array(24).fill(0).map(() => [0]));
</script>

<style>
	@reference "../layout.css";
</style>

<div class="p-8 h-full w-full">
	<div class="flex gap-4 h-[400px] overflow-x-auto p-4 bg-slate-900/30 rounded-3xl border border-white/5">
		{#if browser}
			{#each dmxValues as _, i}
				<div class="flex flex-col items-center gap-3 w-16 h-full border border-white/5 py-4 rounded-xl bg-black/20">
					<span class="text-[9px] font-mono text-slate-500">{i + 1}</span>

					<Slider.Root
						bind:value={dmxValues[i]}
						max={255}
						orientation="vertical"
						class="relative flex flex-col items-center flex-1 w-full touch-none select-none px-4 cursor-pointer"
					>
						<Slider.Track class="relative w-3 grow rounded-full bg-slate-800">
							<Slider.Range class="absolute w-full bg-cyan-500 shadow-[0_0_15px_rgba(6,182,212,0.4)]" />
						</Slider.Track>
						<Slider.Thumb
							class="block w-8 h-4 bg-white border-2 border-cyan-500 rounded-sm hover:scale-125 transition-transform outline-none z-50 shadow-2xl"
						/>
					</Slider.Root>

					<span class="text-[10px] font-mono text-cyan-500">{dmxValues[i][0]}</span>
				</div>
			{/each}
		{/if}
	</div>
</div>