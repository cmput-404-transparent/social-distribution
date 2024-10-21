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
    <div className='grid grid-flow-row auto-rows-max left max-w-max px-[20px] py-[20px] border-r-2 min-h-screen space-y-8'>
      <div className='text-sky-400 text-xl font-bold'>&lt;SocialDistribution /&gt;</div>
      <NavLink to="/stream" className="align-middle grid grid-flow-col auto-cols-max">
        <HomeIcon />
        <p className='pl-3'>Stream</p>
      </NavLink>
      <NavLink to="/search" className="align-middle grid grid-flow-col auto-cols-max">
        <SearchIcon />
        <p className='pl-3'>Search</p>
      </NavLink>
      <NavLink to="/make-post" className="align-middle grid grid-flow-col auto-cols-max">
        <ControlPointIcon />
        <p className='pl-3'>Post</p>
      </NavLink>
      <NavLink to="/notifications" className="align-middle grid grid-flow-col auto-cols-max">
        <CircleNotificationsIcon />
        <p className='pl-3'>Notifications</p>
      </NavLink>
      <div className="align-middle grid grid-flow-col auto-cols-max cursor-pointer" onClick={toProfile}>
        <AccountCircleIcon />
        <p className='pl-3'>Profile</p>
      </div>
    </div>
  )
}
