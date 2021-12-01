import React, { useRef, useState, useEffect } from 'react'
import axios from 'axios';
 import lerp from 'lerpjs'
const Canvas = () => {
const canvasRef = useRef(null)
const [tiles, setTiles] = useState(null)
 const draw = context => {
    
    context.fillStyle = '#000000'
    context.beginPath()
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
    Object.values(tiles).map(t => Object.values(t)
                        .map(
                            v => {
                            let interp = (v[Object.keys(v)[2]]).h
                            if ((v[Object.keys(v)[2]]).h < 0) {
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
                                context.fillRect((v[Object.keys(v)[0]]).x*tileSize,(v[Object.keys(v)[1]]).y*tileSize,tileSize,tileSize)


                            }
                        
            )) 

 } 
  useEffect(() => {

    const interval = setInterval(() => {
    const apiURL = 'http://localhost:9090/map'
          axios.get(apiURL).then((response) => {
                  setTiles(response.data)
          })
    const canvas = canvasRef.current
    const context = canvas.getContext('2d')
    context.fillStyle = '#FFFFFF'
    context.fillRect(0, 0, context.canvas.width, context.canvas.height)
    tiles && draw(context)
        }, 1000);
  return () => clearInterval(interval);
  }, [tiles])
  
        return (
                <canvas width={800} height={600} ref={canvasRef}/>
        );
}
export default Canvas
