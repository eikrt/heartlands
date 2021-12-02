import React, { useRef, useState, useEffect } from 'react'
import axios from 'axios';
import lerp from 'lerpjs'
import '../style/App.css';
import io from 'socket.io-client'

const Canvas = () => {
const canvasRef = useRef(null)
const [tiles, setTiles] = useState(null)
const [x, setX] = useState(0)
const [y, setY] = useState(0)
const step = 32
const tileSize=16
const ENDPOINT = process.env.NODE_ENV == 'development' ? 'http://127.0.0.1:5000' : 'https://eikrt.com/heartlands/ws'

const socket = io.connect(ENDPOINT);
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
const draw = context => {
    
    context.fillStyle = '#000000'
    const sr_grass=0, sg_grass = 125, sb_grass = 0
    const tr_grass = 140, tg_grass = 70, tb_grass = 20
    const sr_water = 0, sg_water = 0, sb_water = 140
    const tr_water = 64, tg_water = 224, tb_water = 208
    let sr = sr_grass, sg = sg_grass, sb = sb_grass
    let tr = tr_grass, tg = tg_grass, tb = tb_grass
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
                                context.fillRect(x + (v[Object.keys(v)[0]]).x*tileSize,y + (v[Object.keys(v)[1]]).y*tileSize,tileSize,tileSize)


                            }
                        
            )) 

 } 
  useEffect(() => {
    canvas = canvasRef.current
    context = canvas.getContext('2d')
    let apiCallTime = 100
    let apiCallChange = 0

           socket.on("map", data => {
                setTiles(data);
          });
          const interval = setInterval(() => {
          apiCallChange += 10

            if (apiCallChange > apiCallTime) {
                socket.emit("map", {x: -x/tileSize, y: -y/tileSize}) 
                apiCallChange = 0
          }
          context.fillStyle = '#000000'
          context.fillRect(0, 0, context.canvas.width, context.canvas.height)
          tiles && draw(context)
        }, 10);
  return () => clearInterval(interval);
  })
       return (
                <div>
                    <div className="mainCanvasContainer">
                        <canvas className="mainCanvas" width={1280} height={640} ref={canvasRef}/>
                    </div>
                    <div className="controlPanel">

                    <button className="controlButton" onClick={controlUp}> up </button>
                    <button className="controlButton" onClick={controlDown}> down </button>
                    <button className="controlButton" onClick={controlLeft}> left </button>
                    <button className="controlButton" onClick={controlRight}> right </button>
                    </div>
                </div>
        );
}
export default Canvas
