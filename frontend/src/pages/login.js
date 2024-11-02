import { useState } from 'react';
import getCookie from '../getCSRFToken';
import { NavLink } from 'react-router-dom';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();

    const data = new URLSearchParams();
    data.append('username', username);
    data.append('password', password);

    const csrftoken = getCookie('csrftoken');

    try {
      const response = await fetch('/api/authors/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrftoken,
        },
        body: data.toString(),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('authToken', data.token); // Store token
        localStorage.setItem('authorId', data.userId);
        window.location.href = "/stream";
      } else {
        alert('Invalid credentials');
      }
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <div className='page'>
      <div className='border h-fit p-9 rounded-[10px]'>
        <h2 className='text-2xl font-bold pb-3'>Login</h2>
        <form onSubmit={handleLogin}>
          <div className='grid grid-rows-4 space-y-3'>
            <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className='border rounded p-2'
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
