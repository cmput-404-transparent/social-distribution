import {NavLink} from 'react-router-dom';
import HomeIcon from '@mui/icons-material/Home';
import ControlPointIcon from '@mui/icons-material/ControlPoint';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

export default function NavBar() {
    return(
        <div className='grid grid-flow-row auto-rows-max left max-w-max px-[20px] 
            py-[20px] border-r-2 min-h-screen space-y-8'>
            <div className='text-sky-400 text-xl font-bold'>&lt;SocialDistribution /&gt;</div>
            <NavLink to="/stream" className="align-middle grid grid-flow-col auto-cols-max">
                <HomeIcon />
                <p className='pl-3'>Stream</p>
            </NavLink>
            <NavLink to="/" className="align-middle grid grid-flow-col auto-cols-max">
                <ControlPointIcon />
                <p className='pl-3'>Post</p>
            </NavLink>
            <NavLink to="/profile" className="align-middle grid grid-flow-col auto-cols-max">
                <AccountCircleIcon />
                <p className='pl-3'>Profile</p>
            </NavLink>
        </div>
    )
}
