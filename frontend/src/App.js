import NavBar from './components/navbar';
import './App.css';
import {BrowserRouter as Router, Routes, Route} from "react-router-dom";
import StreamPage from './pages/stream';
import MakePost from './pages/makePost';
import Profile from './pages/profile';
import ProtectedRoute from './components/protectedRoute';
import Login from './pages/login';
import SignUp from './pages/signup';
import EditProfile from './pages/editProfile';


function App() {

  const authorId = localStorage.getItem('authorId');

  return (
    <Router>
      <div className='grid grid-cols-[auto,1fr] w-full'>
        <NavBar />
        <Routes>
          <Route path="/stream" element={<StreamPage/>} />
          <Route path="/make-post" element={
            <ProtectedRoute>
              <MakePost />
            </ProtectedRoute>
          } />
          <Route path={`/authors/${authorId}`} element={
            <ProtectedRoute>
              <Profile/>
            </ProtectedRoute>
          } />
          <Route path={`/authors/${authorId}/edit`} element={
            <ProtectedRoute>
              <EditProfile/>
            </ProtectedRoute>
          } />
          <Route path="/login" element={<Login/>} />
          <Route path="/signup" element={<SignUp/>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
