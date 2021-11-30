<script>
    import { onMount } from "svelte"
    import { apiData, tiles } from './store.js'
    import { Canvas, Layer, t } from "svelte-canvas";
    import lerp from 'lerpjs'    
    $: render = ({ context, width, height}) => {
                    
        const tileSize=16
        const sr_grass = 0
        const sg_grass = 125
        const sb_grass = 0
        const tr_grass = 140
        const tg_grass = 70
        const tb_grass = 20

        const sr_water = 0
        const sg_water = 0
        const sb_water = 140
        const tr_water = 64
        const tg_water = 224
        const tb_water = 208
        let sr = sr_grass
        let sg = sg_grass
        let sb = sb_grass
        let tr = tr_grass
        let tg = tg_grass
        let tb = tb_grass

        for (let i = 0; i < $tiles.length; i++) {

        let interp = $tiles[i][2].h
        if ($tiles[i][2].h < 0) {
            sr = sr_water
            sg = sg_water
            sb = sb_water
            tr = tr_water
            tg = tg_water
            tb = tb_water
            interp *= 4

            }
        else {
            
            sr = sr_grass
            sg = sg_grass
            sb = sb_grass
            tr = tr_grass
            tg = tg_grass
            tb = tb_grass
            interp *= 4
        }

            context.fillStyle=`rgb(${lerp(sr,tr,interp)},${lerp(sg,tg,interp)},${lerp(sb,tb,interp)})`

        context.fillRect($tiles[i][0].x*tileSize,$tiles[i][1].y*tileSize,tileSize,tileSize)
        }
 };

        onMount(async() => {
             const API_URL = 'http://localhost:9090' 
             fetch(`${API_URL}/map`)
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
        <Canvas width=3200 height=3200> 
            <Layer {render} />
        </Canvas>

</main>
<style>

</style>
