import React, { useRef, useState, useEffect } from 'react'
import lerp from 'lerpjs'
import '../style/App.css';
const Canvas = () => {
const canvasRef = useRef(null)
const [map, setMap] = useState(null)
const [x, setX] = useState(0)
const [y, setY] = useState(0)
const [scale, setScale] = useState(4)
const step = 128
const tileSize=32
const ENDPOINT = process.env.NODE_ENV == 'development' ? 'ws://127.0.0.1:5000' : 'wss://eikrt.com/heartlands/ws/'
const socket = useRef(null)

let canvas = null
let context = null
const controlUp = () => {
        setY(y + step)

}

const controlDown = () => {
        setY(y - step)

}

const controlLeft = () => {
        setX(x + step)
}

const controlRight = () => {
        setX(x - step)

}
const draw = ( context, tiles)  => {
    
    context.fillStyle = '#000000'
    const sr_grass=0, sg_grass = 125, sb_grass = 0
    const tr_grass = 0, tg_grass = 100, tb_grass = 0
    const sr_water = 0, sg_water = 0, sb_water = 140
    const tr_water = 64, tg_water = 224, tb_water = 208
    
    const sr_permafrost= 132, sg_permafrost= 115, sb_permafrost= 140
    const tr_permafrost= 255, tg_permafrost= 255, tb_permafrost= 255

    const sr_mountain_land = 90 , sg_mountain_land= 140, sb_mountain_land= 100
    const tr_mountain_land= 255, tg_mountain_land= 255, tb_mountain_land= 255
    const sr_coarse_land= 142, sg_coarse_land= 143, sb_coarse_land= 113
    const tr_coarse_land= 110, tg_coarse_land= 115, tb_coarse_land= 90
    const sr_sand= 240, sg_sand= 245, sb_sand= 130
    const tr_sand= 85, tg_sand= 85, tb_sand= 85
    const sr_savannah_land= 200, sg_savannah_land= 220, sb_savannah_land= 90
    const tr_savannah_land= 120, tg_savannah_land= 120, tb_savannah_land= 90
    const sr_red_sand= 255, sg_red_sand= 255, sb_red_sand= 115
    const tr_red_sand= 130, tg_red_sand= 90, tb_red_sand= 90
    const sr_ice= 200, sg_ice= 220, sb_ice= 215
    const tr_ice= 255, tg_ice= 255, tb_ice= 255
    let sr = sr_grass, sg = sg_grass, sb = sb_grass
    let tr = tr_grass, tg = tg_grass, tb = tb_grass
    Object.values(tiles)[0].map(t => Object.values(t)
                        .map(
                            v => {
                            let interp = (v[Object.keys(v)])[2].h
                            if ((v[Object.keys(v)])[2].h < Object.values(tiles)[1].sealevel) {
                                sr = sr_water
                                sg = sg_water
                                sb = sb_water
                                tr = tr_water
                                tg = tg_water
                                tb = tb_water
                                interp /= 2
                            }
                            else {
                                    
                                if ((v[Object.keys(v)])[3].type == 'water') {
                                    sr = sr_water
                                    sg = sg_water
                                    sb = sb_water
                                    tr = tr_water
                                    tg = tg_water
                                    tb = tb_water
                                    interp /= 4
                                }
                                else if ((v[Object.keys(v)])[3].type == 'grass') {
                                    sr = sr_grass
                                    sg = sg_grass
                                    sb = sb_grass
                                    tr = tr_grass
                                    tg = tg_grass
                                    tb = tb_grass
                                }
                                else if ((v[Object.keys(v)])[3].type == 'permafrost') {
                                    sr = sr_permafrost
                                    sg = sg_permafrost
                                    sb = sb_permafrost
                                    tr = tr_permafrost
                                    tg = tg_permafrost
                                    tb = tb_permafrost
                                }
                                else if ((v[Object.keys(v)])[3].type == 'mountain_land') {
                                    sr = sr_mountain_land
                                    sg = sg_mountain_land
                                    sb = sb_mountain_land
                                    tr = tr_mountain_land
                                    tg = tg_mountain_land
                                    tb = tb_mountain_land
                                }

                                else if ((v[Object.keys(v)])[3].type == 'coarse_land') {
                                    sr = sr_coarse_land
                                    sg = sg_coarse_land
                                    sb = sb_coarse_land
                                    tr = tr_coarse_land
                                    tg = tg_coarse_land
                                    tb = tb_coarse_land
                                }

                                else if ((v[Object.keys(v)])[3].type == 'savannah_land') {
                                    sr = sr_savannah_land
                                    sg = sg_savannah_land
                                    sb = sb_savannah_land
                                    tr = tr_savannah_land
                                    tg = tg_savannah_land
                                    tb = tb_savannah_land
                                }
                                else if ((v[Object.keys(v)])[3].type == 'sand') {
                                    sr = sr_sand
                                    sg = sg_sand
                                    sb = sb_sand
                                    tr = tr_sand
                                    tg = tg_sand
                                    tb = tb_sand
                                }
                                else if ((v[Object.keys(v)])[3].type == 'ice') {
                                    sr = sr_ice
                                    sg = sg_ice
                                    sb = sb_ice
                                    tr = tr_ice
                                    tg = tg_ice
                                    tb = tb_ice
                                }

                                else if ((v[Object.keys(v)])[3].type == 'red_sand') {
                                    sr = sr_red_sand
                                    sg = sg_red_sand
                                    sb = sb_red_sand
                                    tr = tr_red_sand
                                    tg = tg_red_sand
                                    tb = tb_red_sand

                                }
                                    interp *= 1
                            }
                                context.fillStyle=`rgb(${lerp(sr,tr,interp)},${lerp(sg,tg,interp)},${lerp(sb,tb,interp)})`
                                context.fillRect((x + (v[Object.keys(v)])[0].x*tileSize)/scale, (y + (v[Object.keys(v)])[1].y*tileSize)/scale,tileSize/scale,tileSize/scale)


                            }
                        
            ))
 } 

useEffect(() => {
        socket.current = new WebSocket(ENDPOINT)
        socket.current.onopen = function (event) {
                console.log("socket opened")
                socket.current.send(JSON.stringify({x: -x/tileSize, y: -y/tileSize}))
        }
        socket.current.onclose = () => {
                console.log("socket closed")
        }


return () => socket.current.close() 
}, []) 
useEffect(() => {
        if (!socket.current) return;

        socket.current.onmessage = function (event) {
                const interval = setTimeout(() => {
                if (event.data !== null) {
                    setMap(JSON.parse(event.data))

                }

                }, 1000)
       }
    }, []);
  useEffect(() => {
    canvas = canvasRef.current
    context = canvas.getContext('2d')
          const sTime = 100
          let sChange = 0
          const interval = setInterval(() => {
          sChange += 10
          if (sChange > sTime) {
                socket.current.readyState === 1 && socket.current.send(JSON.stringify({x: -x/tileSize, y: -y/tileSize}))
                sChange = 0
             }
          context.fillStyle = '#000000'
          context.fillRect(0, 0, context.canvas.width, context.canvas.height)
          map && draw(context, map)
        }, 10);
  return () => clearInterval(interval);
  })
       return (
                <div>
                    <div className="mainCanvasContainer">
                        <canvas className="mainCanvas" width={window.innerWidth} height={window.innerHeight} ref={canvasRef}/>
                    </div>
                    <div className="controlPanel">

                    <button className="controlButton" onClick={controlUp}> up </button>
                    <button className="controlButton" onClick={controlDown}> down </button>
                    <button className="controlButton" onClick={controlLeft}> left </button>
                    <button className="controlButton" onClick={controlRight}> right </button>
                    <input type="number" id="scale" value={scale} onChange={(e) => {setScale(e.target.value)}}/>
                    </div>
                </div>
        );
}
export default Canvas
