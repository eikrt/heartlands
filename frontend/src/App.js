import './style/App.css';
import Canvas from './components/Canvas.js';
import {Helmet} from "react-helmet"
function App() {
  return (
    <div>
        <Helmet>

            <meta charSet='utf-8'/>
            <meta name="description" content="Into The Great Wide Open" />
            <title>HEARTLANDS</title>
            
        </Helmet>
          <h1> HEARTLANDS </h1>
            <Canvas></Canvas>
    </div>
  );
}

export default App;
