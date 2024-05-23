<script setup>
import { RouterLink, RouterView } from 'vue-router'

</script>

<template>

	<div class="navbar-container">
		<header>
			<div class="navbar-div">

				<nav class="navbar">
					<RouterLink to="/admin">Admin</RouterLink>|
					<RouterLink to="/">Home</RouterLink>|
					<RouterLink to="/statistics">Stats</RouterLink>
				</nav>
			</div>
		</header>
		
	</div>
	<RouterView/>
		
</template>

<style scoped>
.navbar-container {
	display: flex;
	justify-content: column;
}

.navbar-div {
	display: flex;
	justify-content: center;
}

.navbar {
	display: flex;
	justify-content: space-between;
	width: fit-content;
	background-color: #636363;
}

</style>
