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
    <h1>Settings Component</h1>
</main>