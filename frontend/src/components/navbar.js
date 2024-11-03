/* hover effects from https://tailwindcss.com/docs/hover-focus-and-other-states */

import { NavLink, useLocation } from 'react-router-dom';
import HomeIcon from '@mui/icons-material/Home';
import ControlPointIcon from '@mui/icons-material/ControlPoint';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SearchIcon from '@mui/icons-material/Search';
import { useNavigate } from 'react-router-dom';
import CircleNotificationsIcon from '@mui/icons-material/CircleNotifications';
import LogoutIcon from '@mui/icons-material/Logout';

export default function NavBar() {

  const getAuthorId = () => {
    return localStorage.getItem('authorId');
  }

  const navigate = useNavigate();
  const location = useLocation();

  function toProfile() {
    let link = "/authors/" + getAuthorId();
    navigate(link);
  }

  function logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('authorId');
    navigate('/login');
  }

  return (
    <div className='grid grid-rows-auto min-h-screen bg-customYellow'>
      <div className='grid grid-flow-row auto-rows-max left max-w-max px-[30px] py-[20px] space-y-8'>

        <div className='text-customOrange text-xl font-bold md:block flex justify-center'>
           <p className='hidden md:inline'>&lt;SocialDistribution /&gt;</p>
           <p className='md:hidden'>&lt;/&gt;</p>
         </div>

        <NavLink to="/stream" className="align-middle grid grid-flow-col auto-cols-max">
          <span className="flex items-center justify-left w-30 p-4 rounded-full hover:bg-orange-500/20 transition duration-300 ">
            <HomeIcon />
            <p className='hidden md:inline pl-3'>Stream</p>
          </span>
        </NavLink>

        <NavLink to="/search" className="align-middle grid grid-flow-col auto-cols-max">
          <span className="relative flex items-center justify-center p-4 rounded-full hover:bg-orange-500/20 transition duration-300">
            <SearchIcon />
            <p className='hidden md:inline pl-3'>Search</p>
          </span>
        </NavLink>

        <NavLink to="/make-post" className="align-middle grid grid-flow-col auto-cols-max">
          <span className="relative flex items-center justify-center p-4 rounded-full hover:bg-orange-500/20 transition duration-300">
            <ControlPointIcon />
            <p className='hidden md:inline pl-3'>Post</p>
          </span>
        </NavLink>

        <NavLink to="/notifications" className="align-middle grid grid-flow-col auto-cols-max">
          <span className="relative flex items-center justify-center p-4 rounded-full hover:bg-orange-500/20 transition duration-300">
            <CircleNotificationsIcon />
            <p className='hidden md:inline pl-3'>Notifications</p>
          </span>
        </NavLink>

        <div className="align-middle grid grid-flow-col auto-cols-max cursor-pointer" onClick={toProfile} >
          <span className="relative flex items-center justify-center p-4 rounded-full hover:bg-orange-500/20 transition duration-300">
            <AccountCircleIcon />
            <p className='hidden md:inline pl-3'>Profile</p>
          </span>
        </div>
      </div>

      <div className='h-full flex flex-col justify-end px-[20px] py-[20px]'>
        <div className='align-middle grid grid-flow-col auto-cols-max cursor-pointer' onClick={logout}>
          <span className="relative flex items-center justify-center p-4 rounded-full hover:bg-orange-500/20 transition duration-300">
            <LogoutIcon />
            <p className='hidden md:inline pl-3'>Logout</p>
          </span>
        </div>
      </div>
    </div>
  )
}
