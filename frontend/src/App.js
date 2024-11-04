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
import Search from './pages/search';
import { useEffect } from 'react';
import Notifications from './pages/notifications';
import SharePost from './components/SharePost';


function App() {

  const authorId = localStorage.getItem('authorId');

  useEffect(() => {
    fetch(`/api/posts/${authorId}/github/`)
  });

  return (
    <Router>
      <div className='grid grid-cols-[auto,1fr] w-full gap-0 mx-0'>
        <NavBar />
        <Routes>
          <Route path="/stream" element={<StreamPage/>} />
          <Route path="/make-post" element={
            <ProtectedRoute>
              <MakePost />
            </ProtectedRoute>
          } />
          <Route path="/authors/:profileAuthorId" element={
            <ProtectedRoute>
              <Profile/>
            </ProtectedRoute>
          } />
          <Route path={`/authors/${authorId}/edit`} element={
            <ProtectedRoute>
              <EditProfile/>
            </ProtectedRoute>
          } />
          <Route path={`/authors/:author_id/posts/:post_id`} element={
          <ProtectedRoute>
              <SharePost/>
          </ProtectedRoute>
          } />

          <Route path="/login" element={<Login/>} />
          <Route path="/signup" element={<SignUp/>} />
          <Route path="/search" element={<Search/>} />
          <Route path="/notifications" element={<Notifications/>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
