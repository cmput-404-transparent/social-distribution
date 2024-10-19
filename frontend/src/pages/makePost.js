import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './makePost.css';
import getCookie from '../getCSRFToken';
import commonmark from 'commonmark';
import { Parser, HtmlRenderer } from 'commonmark';


const MakePost = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [content, setContent] = useState('');
  const [contentType, setContentType] = useState('text/plain');
  const [uploadedImage, setImage] = useState('')

  const csrftoken = getCookie('csrftoken');
  const authorId = localStorage.getItem('authorId');

  const navigate = useNavigate();
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {

      const data = new URLSearchParams();
      data.append('title', title);
      data.append('description', description);

      if (contentType === 'text/plain'){
      data.append('contentType', 'text/plain');
      data.append('content', content);
      }

      //commonmark reference - https://github.com/commonmark/commonmark.js/
      else if(contentType === 'text/markdown'){
      const reader = new Parser();
      const writer = new HtmlRenderer();
      const parsed = reader.parse(content);
      var result = writer.render(parsed);
      data.append('contentType', 'text/markdown');
      data.append('content', result);
      }

      else if(contentType === 'image' && uploadedImage){
        const ImageData = await ImageReader(uploadedImage)
        
        data.append('contentType',uploadedImage.type );
        data.append('content', ImageData);
        console.log(uploadedImage.type)
           
      }
      
      const response = await fetch(`/api/authors/${authorId}/posts/create/`, {

        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrftoken,
        },
        body: data.toString()
      });

      console.log('Post created:', response.data);
      navigate('/stream');
    } 
    catch (error) {
      console.error('Error:', error.response ? error.response.data : error.message);
    }
  };

  //Reference for promise - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise 
  //Reference for Filereader - https://stackoverflow.com/questions/71748138/how-do-i-convert-image-file-to-base64, https://www.youtube.com/watch?v=EPlXPdNvQEY
  const ImageReader = (image) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result)
      reader.onerror = (error) => reject(error);
      reader.readAsDataURL(image);
    })
  }

  return (
    <div className="post-div div-make-post">
      <h1 className='post-title'>Make a Post</h1>
      <form onSubmit={handleSubmit} className='form-make-post'>
        <div className='div-make-post'>
          <label className='label-make-post'>Title:</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            className='input-make-post'
          />
        </div>
        <div className='div-make-post'>
          <label>Description:</label>
          <input
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </div>

        <label> Content Type:</label>
        <button className='div-plain' type = "button" onClick={() => setContentType('text/plain')}>Plain Text</button>
        <button className='div-markdown' type = "button" onClick={() => setContentType('text/markdown')}>MarkDown</button>
        <button className='div-image' type = "button" onClick={() => setContentType('image')}>Image</button>
        <br></br><br></br>

        <label>Content:</label>
        
        <div className='div-make-post'>

          {contentType === 'image' ? (
          <><label>Upload File</label><input type="file" id="imageInput" onChange={(e) => setImage(e.target.files[0])}
          required></input></>):
          (
            
          <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          required
          className='make-post-textarea'
          
          />

          )}
          
        </div>
        <button type="submit" className='make-post-button'>Create Post</button>
      
      </form>
    </div>
  );
};

export default MakePost;
