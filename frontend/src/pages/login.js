import { useState } from 'react';
import getCookie from '../getCSRFToken';
import { NavLink } from 'react-router-dom';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [host, setHost] = useState('');

  // for local/remote toggle
  const [authorLocation, setAuthorLocation] = useState('local');
  const handleChange = (event, loc) => {
    setAuthorLocation(loc);
    setHost('');
  };

  const handleLogin = async (e) => {
    e.preventDefault();

    const data = new URLSearchParams();
    data.append('host', host);
    data.append('username', username);
    data.append('password', password);

    const csrftoken = getCookie('csrftoken');

    let loginURL = '/api/authors/login/';
    if (host !== "") {
      loginURL = '/api/authors/remote-nodes/';
    }

    try {
      const response = await fetch(loginURL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrftoken,
          'Authorization': `Basic ${localStorage.getItem('authToken')}`,
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
  };

  return (
    <div className='page'>
      <div className='border h-fit p-9 rounded-[10px]'>
        <h2 className='text-2xl font-bold pb-3'>Login</h2>

        <ToggleButtonGroup color="warning" value={authorLocation} exclusive onChange={handleChange} className='pb-3'>
          <ToggleButton value="local">Local</ToggleButton>
          <ToggleButton value="remote">Remote</ToggleButton>
        </ToggleButtonGroup>

        <form onSubmit={handleLogin}>
          <div className='grid grid-rows-4 space-y-3'>
            {
              (authorLocation === "remote") && (
                <input
                  type="text"
                  placeholder="Remote Host"
                  value={host}
                  onChange={(e) => setHost(e.target.value)}
                  required
                  className='border rounded p-2 mt-3'
                />
              ) 
            }
            <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className={`border rounded p-2 ${authorLocation === "local"? "mt-3": ""}`}
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className='border rounded p-2'
            />
            <button type="submit" className='bg-customOrange rounded'>Login</button>
            <p>
              Don't have an account?
              <NavLink to="/signup" className='text-customOrange'> Sign Up</NavLink>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
