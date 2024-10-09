import NavBar from './components/navbar';
import './App.css';
import {BrowserRouter as Router, Routes, Route} from "react-router-dom";
import StreamPage from './pages/stream';

function App() {
  return (
    <Router>
      <div className='grid grid-cols-[auto,1fr] w-full'>
        <NavBar />
        <Routes>
          <Route path="/" element={<StreamPage/>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
