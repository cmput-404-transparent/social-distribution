import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './makePost.css';
import getCookie from '../getCSRFToken';


const MakePost = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [content, setContent] = useState('');

  const csrftoken = getCookie('csrftoken');
  const authorId = localStorage.getItem('authorId');

  const navigate = useNavigate();
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {

      const data = new URLSearchParams();
      data.append('title', title);
      data.append('description', description);
      data.append('contentType', 'text/plain');
      data.append('content', content);

      const response = await fetch(`/api/posts/authors/${authorId}/posts/create/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrftoken,
        },
        body: data.toString()
      });

      console.log('Post created:', response.data);
      navigate('/stream');
    } catch (error) {
      console.error('Error:', error.response ? error.response.data : error.message);
    }
  };

  return (
    <div className="post-div">
      <h1>Make a Post</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Title:</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Description:</label>
          <input
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </div>

        <label>Content:</label>

        <div>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
          />
        </div>
        <button type="submit">Create Post</button>

      </form>
    </div>
  );
};

export default MakePost;