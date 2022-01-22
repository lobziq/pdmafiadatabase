<script>
    import { link } from "svelte-routing";
</script>

<main>
    <nav class="navbar" aria-label="main navigation">
        <div class="navbar-menu align-center">
            <a href="/"class="navbar-item">Игроки</a>
            <a href="/" class="navbar-item">Игры</a>
            <a href="settings" use:link replace class="navbar-item">Сеттинги</a>
            <a href="/" class="navbar-item">👁️</a>
        </div>
    </nav>
</main>

<style>
</style>
