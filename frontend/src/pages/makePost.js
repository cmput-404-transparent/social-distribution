import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './makePost.css';


const MakePost = () => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [content, setContent] = useState('');
    const [authorId, setAuthorId] = useState(1); // placeholder untill login


    const navigate = useNavigate();
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post(
                `http://localhost:8000/posts/authors/${authorId}/posts/create/`, 
                {
                    title,
                    description,
                    contentType: 'text/plain', 
                    content,
                }
            );
            console.log('Post created:', response.data);
            navigate('/'); 
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