<script lang="ts">
    // DAS IST DIE ENTSCHEIDENDE ZEILE.
    // Sie sagt Svelte, wo deine Tailwind-Styles liegen.
    // Wir gehen davon aus, dass layout.css im 'src' Ordner liegt (eins höher als routes).
    import "./layout.css";

    // Svelte 5 Syntax um den Inhalt der Seite anzuzeigen
    let { children } = $props();
</script>

{@render children()}