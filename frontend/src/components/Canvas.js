// This file holds functionalities to draw and interact with canvas

import React, { useRef, useState, useEffect } from 'react'
import lerp from 'lerpjs'
import '../style/App.css';
const Canvas = () => {
const canvasRef = useRef(null)
const [map, setMap] = useState(null)
const [x, setX] = useState(0)
const [y, setY] = useState(0)
const [scale, setScale] = useState(4)
const [receivedPacket, setReceivedPacket] = useState(false)
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


    // tile colors and values towards they will be scaled to
    const sr_grass=125, sg_grass = 65, sb_grass = 48
    const tr_grass = 40, tg_grass = 0, tb_grass = 20
    const sr_water = 240, sg_water = 100, sb_water = 50
    const tr_water = 240, tg_water = 100, tb_water = 30
    
    const sr_permafrost= 287, sg_permafrost= 3, sb_permafrost= 48
    const tr_permafrost= 287, tg_permafrost= 3, tb_permafrost= 20

    const sr_mountain_land = 142 , sg_mountain_land= 31, sb_mountain_land= 148
    const tr_mountain_land= 142, tg_mountain_land= 31, tb_mountain_land= 148
    const sr_coarse_land= 69, sg_coarse_land= 12, sb_coarse_land= 52
    const tr_coarse_land= 69, tg_coarse_land= 0, tb_coarse_land= 22
    const sr_sand= 61, sg_sand= 95, sb_sand= 80
    const tr_sand= 61, tg_sand= 15, tb_sand= 50
    const sr_savannah_land= 51, sg_savannah_land= 36, sb_savannah_land= 50
    const tr_savannah_land= 51, tg_savannah_land= 16, tb_savannah_land= 22
    const sr_red_sand= 34, sg_red_sand= 36, sb_red_sand= 62
    const tr_red_sand= 34, tg_red_sand= 5, tb_red_sand= 50
    const sr_ice= 193, sg_ice= 36, sb_ice= 78
    const tr_ice= 78, tg_ice= 36, tb_ice= 100
    const sr_void = 1, sg_void = 1, sb_void = 0
    const tr_void = 1, tg_void = 1, tb_void = 0
    let sr = sr_void, sg =  sg_void, sb = sb_void
    let tr = tr_void, tg = tg_void, tb = tb_void 
    Object.values(tiles)[0].map(t => Object.values(t)
                        .map(
                            v => {
                            let interp = (v[Object.keys(v)])[2].h
                  
                                    
                                if ((v[Object.keys(v)])[3].type == 'void') {
                                    sr = sr_void
                                    sg = sg_void
                                    sb = sb_void
                                    tr = tr_void
                                    tg = tg_void
                                    tb = tb_void
                                }
                                else if ((v[Object.keys(v)])[3].type == 'water') {
                                    sr = sr_water
                                    sg = sg_water
                                    sb = sb_water
                                    tr = tr_water
                                    tg = tg_water
                                    tb = tb_water
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
                                if (interp > 1.2) { // if tall enough, lerp into white (snow)
                                    tb = 100
                                    interp /= 2
                                }
                                context.fillStyle=`hsl(${lerp(sr,tr,interp)},${lerp(sg,tg,interp)}%,${lerp(sb,tb,interp)}%)`
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
                setReceivedPacket(true)
                }, 1000)
       }
    }, []);
  useEffect(() => {
    canvas = canvasRef.current

    if (!canvas) {
        return
    }
    context = canvas.getContext('2d')
          const sTime = 100
          let sChange = 0
          const interval = setInterval(() => {
          sChange += 10
          if (sChange > sTime) {
                if (receivedPacket) {
                    if (socket.current.readyState === 1 && receivedPacket) {
                            socket.current.send(JSON.stringify({x: -x/tileSize, y: -y/tileSize}))
                            setReceivedPacket(false)
                    }
                    sChange = 0
                }
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
                     {!map && <div className="loadScreen"><p>Loading...</p></div>}
               {map && <canvas className="mainCanvas" width={window.innerWidth-128} height={window.innerHeight} ref={canvasRef}/>}
                    </div>
                    <div className="controlPanel">

                        <button className="controlButton" onClick={controlUp}> up </button>
                        <button className="controlButton" onClick={controlDown}> down </button>
                        <button className="controlButton" onClick={controlLeft}> left </button>
                        <button className="controlButton" onClick={controlRight}> right </button>
                        <input type="number" id="scale" value={scale} onChange={(e) => {setScale(e.target.value)}}/>
                    </div>
                    <div className="infoPanel">
                        <div className="worldInfoPanel">
                            <h2>World Info</h2>
                            <h3>Name: {map && Object.values(map)[1].name}</h3>
                            <h3>Population: 0</h3>
                        </div>
                    </div>
                </div>
        );
}
export default Canvas
