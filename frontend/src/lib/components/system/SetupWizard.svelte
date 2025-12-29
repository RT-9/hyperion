<script lang="ts">
    import { api } from '$lib/api';

    /**
     * Props:
     * :param onComplete: Callback function triggered when the admin user is successfully created.
     */
    let { onComplete } = $props();

    // Form state
    let formData = $state({
        username: '',
        first_name: '',
        last_name: '',
        password: '',
        password_confirm: ''
    });

    let loading = $state(false);
    let errorMsg = $state<string | null>(null);

    /**
     * Submits the admin creation form to the backend.
     */
    async function handleSubmit(e: Event) {
        e.preventDefault();
        errorMsg = null;

        if (formData.password !== formData.password_confirm) {
            errorMsg = "Passwords do not match.";
            return;
        }

        loading = true;

        try {
            await api('/api/startup/create-admin-user', {
                method: 'POST',
                body: JSON.stringify(formData)
            });
            
            // Notify parent that we are done
            onComplete();
        } catch (err: any) {
            errorMsg = err.message || "Failed to create admin user.";
        } finally {
            loading = false;
        }
    }
</script>

<div class="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-md p-4">
    <div class="w-full max-w-md bg-slate-900 border border-slate-700 rounded-2xl p-8 shadow-2xl relative overflow-hidden">
        
        <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-cyan-500 via-purple-500 to-cyan-500"></div>

        <h2 class="text-2xl font-bold text-white mb-2">Initialise Hyperion</h2>
        <p class="text-slate-400 text-sm mb-6">First run detected. To get started, please create an admin account with a username of your choice and a strong password. </p>

        {#if errorMsg}
            <div class="mb-4 p-3 bg-red-900/30 border border-red-800 text-red-200 text-sm rounded">
                {errorMsg}
            </div>
        {/if}

        <form onsubmit={handleSubmit} class="space-y-4">
            
            <div class="grid grid-cols-2 gap-4">
                <div class="space-y-1">
                    <label class="text-xs font-mono text-slate-500 uppercase">First Name</label>
                    <input 
                        type="text" 
                        required 
                        bind:value={formData.first_name}
                        class="w-full bg-black border border-slate-700 rounded p-2 text-white focus:border-cyan-500 focus:outline-none transition-colors"
                    />
                </div>
                <div class="space-y-1">
                    <label class="text-xs font-mono text-slate-500 uppercase">Last Name</label>
                    <input 
                        type="text" 
                        required
                        bind:value={formData.last_name} 
                        class="w-full bg-black border border-slate-700 rounded p-2 text-white focus:border-cyan-500 focus:outline-none transition-colors"
                    />
                </div>
            </div>

            <div class="space-y-1">
                <label class="text-xs font-mono text-slate-500 uppercase">Username</label>
                <input 
                    type="text" 
                    required 
                    bind:value={formData.username}
                    class="w-full bg-black border border-slate-700 rounded p-2 text-white focus:border-cyan-500 focus:outline-none transition-colors"
                />
            </div>

            <div class="space-y-1">
                <label class="text-xs font-mono text-slate-500 uppercase">Password</label>
                <input 
                    type="password" 
                    required 
                    bind:value={formData.password}
                    class="w-full bg-black border border-slate-700 rounded p-2 text-white focus:border-cyan-500 focus:outline-none transition-colors"
                />
            </div>

            <div class="space-y-1">
                <label class="text-xs font-mono text-slate-500 uppercase">Confirm Password</label>
                <input 
                    type="password" 
                    required 
                    bind:value={formData.password_confirm}
                    class="w-full bg-black border border-slate-700 rounded p-2 text-white focus:border-cyan-500 focus:outline-none transition-colors"
                />
            </div>

            <button 
                type="submit" 
                disabled={loading}
                class="w-full mt-6 py-3 bg-cyan-600 hover:bg-cyan-500 text-white font-bold rounded transition-all disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center gap-2"
            >
                {#if loading}
                    <svg class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                    Creating Admin...
                {:else}
                    Create System Admin
                {/if}
            </button>
        </form>
    </div>
</div>