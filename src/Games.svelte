<script>
	import { Router, Link, Route } from "svelte-routing";
	import Navbar from "./Navbar.svelte";

	export let name;
	export let url = "";
</script>

<Navbar />
<main>
    <h1>Games Component</h1>
</main>