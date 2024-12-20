import { useState } from 'react';
import { TextField } from '@mui/material';
import getCookie from '../getCSRFToken';

export default function SignUp() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [github, setGithub] = useState('');

  const handleSignup = async (e) => {

    e.preventDefault();

    const data = new URLSearchParams();
    data.append('username', username);
    data.append('password', password);
    data.append('displayName', displayName);
    data.append('github', github);
    const url = new URL(window.location.href);
    data.append('origin', url.origin);

    const csrftoken = getCookie('csrftoken');

    try {
      const response = await fetch('/api/authors/signup/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrftoken,
        },
        body: data.toString(),
      });

      if (response.ok) {
        const data = await response.json();
        if (data.detail) {
          alert(data.detail); // Display the pending approval message to the user
        } else {
          localStorage.setItem('authToken', data.token);
          localStorage.setItem('authorId', data.userId);
          window.location.href = "/stream";
        }
      } else {
        const errorData = await response.json();
        alert(errorData.detail || 'Invalid credentials'); // Show error message from server
      }
    } catch (error) {
      console.error('Login failed:', error);
    }
  }

  return(
    <div className='page'>
      <div className='border h-fit p-9 rounded-[10px] w-1/2'>
        <h2 className='text-2xl font-bold pb-3'>Create Account</h2>
        <form onSubmit={handleSignup}>
          <div className='grid auto-rows-auto space-y-3'>
            <TextField
              label="Username"
              onChange={(e) => setUsername(e.target.value)}
              value={username}
              required
            />
            <TextField
              label="Password"
              onChange={(e) => setPassword(e.target.value)}
              value={password}
              required
              type="password"
            />
            <TextField
              label="Display Name"
              onChange={(e) => setDisplayName(e.target.value)}
              value={displayName}
              defaultValue={username}
            />
            <TextField
              label="GitHub Username"
              onChange={(e) => setGithub(e.target.value)}
              value={github}
              helperText="Can be set later"
            />
            <button type="submit" className='bg-customOrange rounded p-3 font-bold'>Sign Up</button>
          </div>
        </form>
      </div>
    </div>
  )
}
