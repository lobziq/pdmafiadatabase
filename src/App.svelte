<script>
	import Navbar from './Navbar.svelte';
	export let name;

</script>

<Navbar/>
<main>
	<h1>Hello {name}!</h1>
	<p>Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn how to build Svelte apps.</p>
</main>

<style>
	main {
		text-align: right;
		padding: 1em;
		max-width: 200px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: lowercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>