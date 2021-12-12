// This file holds functionalities to draw and interact with canvas

import React, { useRef, useState, useEffect } from 'react'
import lerp from 'lerpjs'
import '../style/App.css';
import {startingColors} from '../utils/Colors'
import {targetColors} from '../utils/Colors'
const Canvas = () => {
const canvasRef = useRef(null)
const [renderRange_w, setRenderRange_w] = useState(8)
const [renderRange_h, setRenderRange_h] = useState(8)
const [chunkQueue, setChunkQueue] = useState(0)
const [map, setMap] = useState(null)
const [x, setX] = useState(0)
const [y, setY] = useState(0)
const [ids, setIds] = useState([])
const [scale, setScale] = useState(4)
const [metadata, setMetadata] = useState(null)
const [sendData, setSendData] = useState(false)
const step = 64
const tileSize=32
const defaultChunkSize = 16
const ENDPOINT = process.env.NODE_ENV == 'development' ? 'ws://127.0.0.1:5000' : 'wss://eikrt.com/heartlands/ws/'
const socket = useRef(null)

let canvas = null
let context = null
// controls
const controlUp = () => {

        setIds([])

        setMap({tiles: []})
        setY(prevState => prevState - step)

}

const controlDown = () => {
        
        setIds([])
        
        setMap({tiles: []})
        setY(prevState => prevState + step)
}

const controlLeft = () => {
        setIds([])
        //
        setMap({tiles: []})
        setX(prevState => prevState - step)
}

const controlRight = () => {
        setIds([])
        setMap({tiles: []})
        setX(prevState => prevState + step)

}
// rendering 
const draw = ( context, tiles)  => {
    
    context.fillStyle = '#000000'


    // tile colors and values towards they will be scaled to

    let s = startingColors.void
    let t = targetColors.void
    const mapdata = Object.values(tiles)[0]
    mapdata.map(til => Object.values(til)
                        .map(
                            v => {


                            const vkeys = (v[Object.keys(v)])

                                    if (Math.round(-x + ( ( vkeys[0].x)*tileSize)/scale) > 0 && Math.round(-x + ( ( vkeys[0].x)*tileSize)/scale) < window.innerWidth  ) {

                            const vkeys = (v[Object.keys(v)])
                            let interp = vkeys[2].h
                            const type = vkeys[3].type
                  
                                if (type == 'void') {
                                    s = startingColors.void
                                    t = targetColors.void
                                }
                                else if (type == 'water') {
                                    s = startingColors.water
                                    t = targetColors.water
                                }
                                else if (type == 'grass') {
                                    s = startingColors.grass
                                    t = targetColors.grass
                                }
                                else if (type == 'permafrost') {
                                    s = startingColors.permafrost
                                    t = targetColors.permafrost
                                }
                                else if (type == 'mountain_land') {
                                    s = startingColors.mountain_land
                                    t = targetColors.mountain_land
                                }

                                else if (type == 'coarse_land') {
                                    s = startingColors.coarse_land
                                    t = targetColors.coarse_land
                                }

                                else if (type == 'savannah_land') {
                                    s = startingColors.savannah_land
                                    t = targetColors.savannah_land

                                }
                                else if (type == 'sand') {
                                    s = startingColors.sand
                                    t = targetColors.sand
                                }
                                else if (type == 'ice') {
                                    s = startingColors.ice
                                    t = targetColors.ice
                                }

                                else if (type == 'red_sand') {
                                    s = startingColors.red_sand
                                    t = targetColors.red_sand

                                }
                                if (interp > 1.2) { // if tall enough, lerp into white (snow)
                                    t = targetColors.ice
                                    interp /= 2
                                }
                                context.fillStyle=`hsl(${lerp(s.h,t.h,interp)},${lerp(s.s,t.s,interp)}%,${lerp(s.l,t.l,interp)}%)`
                                context.fillRect(Math.round(-x + ( ( vkeys[0].x)*tileSize)/scale), Math.round(-y + ( + (vkeys[1].y)*tileSize)/scale),tileSize/scale,tileSize/scale)


                            }
                            }
                        
            ))
 } 
// initialize socket
const updateRenderRange = () => {

           const wWidth = window.innerWidth
           const wHeight = window.innerHeight
           const dChunkSize = metadata ? metadata.chunk_size : defaultChunkSize
           setRenderRange_w( wWidth / tileSize / (dChunkSize)*scale) 
           setRenderRange_h(wHeight / tileSize / (dChunkSize)*scale) 
        }
useEffect(() => {
        window.addEventListener('resize', updateRenderRange) 
        socket.current = new WebSocket(ENDPOINT)
        socket.current.onopen = function (event) {
                console.log("socket opened")
                socket.current.send(JSON.stringify({header: 'metadata'}))
        }
        socket.current.onclose = () => {
                console.log("socket closed")
        }


return () => socket.current.close() 
}, [])

// update tile state

useEffect(() => {

        if (socket.current === null) {

                return;
        }

        socket.current.onmessage = (event) => {
                   if (event.data !== null) {
                       const data = JSON.parse(event.data)
                           if (data === null) {
                                   return
                           }
                       if (data.header==='chunks') {

                            setMap(prevState => {
                                    let pState = {...prevState}
                                    if (prevState === null) {
                                            pState = {tiles: []}
                                    }
                                    if (data === null) {
                                            data = {tiles: []}
                                    }


                                const merged = {tiles: pState.tiles.concat(data.tiles)}
                                return merged 
                            })


                        }
                           else if (data.header ==='metadata') {
                                   setMetadata(data.metadata)

                                   //const tx = (i + Math.round(((x/tileSize))/metadata.chunk_size)*scale), ty = (j + Math.round(((y/tileSize))/metadata.chunk_size)*scale)
                                   const tx = 0
                                   const ty = 0
                                   socket.current.send(JSON.stringify({header: 'chunks', x: tx, y: ty}))
                           }
               
                        setChunkQueue(prevState => {
                            return prevState - 1

                        })

            }
        }
}, []);

// filter unneccesary tiles from map
useEffect(() => {
        const tile_ids = []
        if (map) {
                map.tiles = map.tiles.filter( (tile) => {
                const coords = (Object.values(tile)[0].props) 
                const tile_x = (coords[0].x)* tileSize/scale
                const tile_y = (coords[1].y) * tileSize/scale

                const target_y = (y)
                const target_x = (x)
                const buffer = 0 // 32*8*(tileSize/scale) 
                const inBounds = tile_y - target_y >= -buffer && tile_x - target_x >= -buffer && tile_x - target_x <= (metadata.chunk_size * tileSize * renderRange_w + buffer) / scale && tile_y - target_y <= (metadata.chunk_size * tileSize * renderRange_h + buffer) / scale
                
                //const isDuplicate = !tile_ids.includes(coords[4].id)
            /*    const tx = (0 + Math.round(((x/tileSize))/metadata.chunk_size)*scale), ty = (0 + Math.round(((y/tileSize))/metadata.chunk_size)*scale)
                    if (overBounds) {
                       
                                
                    setIds(prevState => {
                    return prevState.filter(_ => {
                        return _[0] !== tx 
                    })
                })
                     }*/
                return inBounds 

                })
    }
}, [map,x,y, renderRange_w, renderRange_h])

// sending which chunks to get
useEffect(() => {
        if (socket.current.readyState === 1 && chunkQueue <= 0 && metadata) {
            for (let i = -2; i < renderRange_w; i++) {
                    for (let j = -2; j < renderRange_h; j++) {

                            const tx = (i + Math.round(((x/tileSize))/metadata.chunk_size)*scale), ty = (j + Math.round(((y/tileSize))/metadata.chunk_size)*scale)
                            if (tx >= 0 && ty >= 0 && !(ids.filter(e => e[0] === tx && e[1] === ty).length > 0)) {
                                socket.current.send(JSON.stringify({header: 'chunks', x: tx, y: ty}))
                                    setChunkQueue(prevState => {
                                            return prevState + 1

                                    })
                                ids.push([tx, ty])
                    }

            }
            
        }
     }
        setSendData(false)
},[sendData])
// main loop, etc
  useEffect(() => {
    canvas = canvasRef.current

    if (!canvas) {
        return
    }
    context = canvas.getContext('2d', {alpha: false}) // alpha off for optimization
          const sTime = 10
          let sChange = 0
          const checkTime = 1000
          let checkChange = 0
          const interval = setInterval(() => {
          sChange += 10

          if (sChange > sTime) {
                    setSendData(true)
                    sChange = 0
                }
          context.fillStyle = '#000000'
          
          //map && map.tiles.length > 2 && context.fillRect(0, 0, context.canvas.width, context.canvas.height)
          map && draw(context, map)
        }, 10);
  return () => clearInterval(interval);
  })
       return (
                <div>

                    <div className="mainCanvasContainer">
                     {!map && <div className="loadScreen"><p>Loading...</p></div>}
               {<canvas className="mainCanvas" width={window.innerWidth-128} height={window.innerHeight} ref={canvasRef}/>}
                    </div>
                    <div className="controlPanel">

                        <button className="controlButton" onClick={controlUp}> up </button>
                        <button className="controlButton" onClick={controlDown}> down </button>
                        <button className="controlButton" onClick={controlLeft}> left </button>
                        <button className="controlButton" onClick={controlRight}> right </button>
                        <input type="number" id="scale" value={scale < 8 ? scale : 8} onChange={(e) => {
                                setScale(e.target.value)
                                updateRenderRange()
                        }}/>
                    </div>
                    <div className="infoPanel">
                        <div className="worldInfoPanel">
                            <h2>World Info</h2>
                            <h3>Name: {metadata && metadata.name}</h3>
                            <h3>Population: 0</h3>
                        </div>
                    </div>
                </div>
        );
}
export default Canvas
