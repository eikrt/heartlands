<script>
        import { onMount } from "svelte"
        import { apiData, tiles } from './store.js'
        onMount(async() => {
                        fetch("http://localhost:9090/map")
                                .then(response => response.json())
                                .then(data => {
                                                apiData.set(data)
                                        })
                                .catch(error => {
                                                console.log(error)

                                        })
                })
</script>

<main>
<h1>HEARTLANDS</h1>
        {#each $tiles as tile}
                <p>{tile[0].x} {tile[1].y} {tile[2].h}<p>
        {/each}
</main>
<style>

</style>
