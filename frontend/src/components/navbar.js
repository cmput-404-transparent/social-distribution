/* hover effects from https://tailwindcss.com/docs/hover-focus-and-other-states */

import { NavLink } from 'react-router-dom';
import HomeIcon from '@mui/icons-material/Home';
import ControlPointIcon from '@mui/icons-material/ControlPoint';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SearchIcon from '@mui/icons-material/Search';
import { useNavigate } from 'react-router-dom';
import CircleNotificationsIcon from '@mui/icons-material/CircleNotifications';

export default function NavBar() {

  const getAuthorId = () => {
    return localStorage.getItem('authorId');
  }

  const navigate = useNavigate();

  function toProfile() {
    let link = "/authors/" + getAuthorId();
    navigate(link);
  }

  return (
    <div className='bg-customYellow grid grid-flow-row auto-rows-max left max-w-max px-[30px] py-[20px] border-r-2 min-h-screen space-y-8'>
      <div className='text-customOrange text-xl font-bold'>&lt;SocialDistribution /&gt;</div>

      <NavLink to="/stream" className="align-middle grid grid-flow-col auto-cols-max pl-4">

      <span className="relative flex items-center justify-center w-30 p-4 rounded-full hover:bg-orange-500/20 transition duration-300 ">
          <HomeIcon />
          <p className='pl-3'>Stream</p>
        </span>
     
      </NavLink>
      <NavLink to="/search" className="align-middle grid grid-flow-col auto-cols-max pl-4">
      <span className="relative flex items-center justify-center p-4 rounded-full hover:bg-orange-500/20 transition duration-300">
          <SearchIcon />
          <p className='pl-3'>Search</p>
        </span>

      </NavLink>
      <NavLink to="/make-post" className="align-middle grid grid-flow-col auto-cols-max pl-4">
      <span className="relative flex items-center justify-center p-4 rounded-full hover:bg-orange-500/20 transition duration-300">
          <ControlPointIcon />
          <p className='pl-3'>Post</p>
        </span>

      </NavLink>
      <NavLink to="/notifications" className="align-middle grid grid-flow-col auto-cols-max pl-4">
        <span className="relative flex items-center justify-center p-4 rounded-full hover:bg-orange-500/20 transition duration-300">
          <CircleNotificationsIcon />
          <p className='pl-3'>Notifications</p>
        </span>

      </NavLink>
      <div className="align-middle grid grid-flow-col auto-cols-max cursor-pointer pl-4" onClick={toProfile} >
         <span className="relative flex items-center justify-center p-4 rounded-full hover:bg-orange-500/20 transition duration-300">
          <AccountCircleIcon />
          <p className='pl-3'>Profile</p>
        </span>

      </div>
    </div>
  )
}
