import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import getCookie from '../getCSRFToken';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const data = new URLSearchParams();
    data.append('username', username);
    data.append('password', password);

  const handleLogin = async (e) => {
    e.preventDefault();
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
        navigate('/stream'); // Redirect to stream
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
          <div className='grid grid-rows-3 space-y-3'>
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
            <button type="submit" className='bg-emerald-400 rounded'>Login</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
