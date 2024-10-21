import { useEffect, useState } from "react";
import { TextField } from '@mui/material';
import getCookie from "../getCSRFToken";
import { useNavigate } from 'react-router-dom';
import UploadIcon from '@mui/icons-material/Upload';


export default function EditProfile() {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [github, setGithub] = useState('');

  const authorId = localStorage.getItem('authorId');

  const navigate = useNavigate();

  useEffect(() => {
    // get profile information
    fetch(`/api/authors/${authorId}/`)
    .then((r) => r.json())
    .then((data) => {
      setUsername(data.username);
      setDisplayName(data.display_name);
      setGithub(data.github);
    })
    // eslint-disable-next-line
  }, []);

  const updateProfile = async (e) => {
    e.preventDefault();

    const data = new URLSearchParams();
    data.append('username', username);
    data.append('password', password);
    data.append('displayName', displayName);
    data.append('github', github);

    const csrftoken = getCookie('csrftoken');

    try {
      const response = await fetch(`/api/authors/${authorId}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrftoken,
        },
        body: data.toString(),
      });

      if (response.ok) {
        navigate(`/authors/${authorId}`);
      } else {
        let r = await response.json();
        let errors = r.errors;
        let message = "Profile not saved. Errors:\n" + errors.join("\n");
        alert(message);
      }
    } catch (error) {
      console.error('Edit profile failed:', error);
    }
  }

  return(
    <div className='page'>
      <div className='border h-fit p-9 rounded-[10px] w-4/5'>
        <h2 className='text-2xl font-bold pb-3'>Edit Profile</h2>
        <div className="flex justify-center justify-items-center align-middle middle">
          <p className="justify-self-center align-middle leading-[inherit]">
            profile picture
          </p>
          <button className="bg-neutral-400 rounded p-2">
            <UploadIcon />
          </button>
        </div>
        <form onSubmit={updateProfile} className="pt-8">
          <div className='grid auto-rows-auto space-y-3'>
            <TextField
              label="Username"
              onChange={(e) => setUsername(e.target.value)}
              value={username}
            />
            <TextField
              label="Password"
              onChange={(e) => setPassword(e.target.value)}
              value={password}
              type="password"
            />
            <TextField
              label="Display Name"
              onChange={(e) => setDisplayName(e.target.value)}
              value={displayName}
              defaultValue={username}
            />
            <TextField
              label="GitHub"
              onChange={(e) => setGithub(e.target.value)}
              value={github}
            />
            <button type="submit" className='bg-sky-400 rounded p-3 font-bold'>Save</button>
          </div>
        </form>
      </div>
    </div>
  )
}
