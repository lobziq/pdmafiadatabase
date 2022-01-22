<script>
	import { Router, Link, Route } from "svelte-routing";
	import Navbar from "./Navbar.svelte";
	import Settings from "./Settings.svelte";
	import Home from "./Home.svelte"

	export let name;
	export let url = "";
</script>

<Navbar />
<main>
	<h1>Hello HOMEPAGE!</h1>
	<p>
		Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn
		how to build Svelte apps.
	</p>
</main>