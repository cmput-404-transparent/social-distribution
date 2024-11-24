import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './makePost.css';
import getCookie from '../getCSRFToken';

import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import CloseIcon from '@mui/icons-material/Close';



/**
 * source: Material UI Documentation
 * link: https://mui.com/material-ui/react-modal/
 * date: November 4, 2024
 */
const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 700,
  bgcolor: 'background.paper',
  border: '1px solid',
  borderRadius: '5px',
  p: 4,
};

const MakePost = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [content, setContent] = useState('');
  const [contentType, setContentType] = useState('text/plain');
  const [uploadedImage, setImage] = useState('')
  const [activeButton, setActiveButton] = useState('plain');
  const [visibility, setVisbility] = useState('PUBLIC');

  const [commonmarkImages, setCommonmarkImages] = useState([]);
  const [commonmarkImage, setCommonmarkImage] = useState('');

  // upload image from <a href="https://www.flaticon.com/free-icons/upload" title="upload icons">Upload icons created by Kiranshastry - Flaticon</a>

  const handleChange = (event) => {
    setVisbility(event.target.value);
  };

  const csrftoken = getCookie('csrftoken');
  const authorId = localStorage.getItem('authorId');

  const navigate = useNavigate();

  useEffect(() => {
    // get all hosted images
    fetch('/api/authors/images/all/', {
      headers: {
        'Authorization': `Basic ${localStorage.getItem('authToken')}`,
      },
    })
      .then(r => r.json())
      .then(data => {
        setCommonmarkImages(data.images)
      })
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {

      const data = new URLSearchParams();
      data.append('title', title);
      data.append('description', description);
      data.append('visibility', visibility);

      if (contentType === 'text/plain') {
        data.append('contentType', 'text/plain');
        data.append('content', content);
      }

      else if (contentType === 'text/markdown') {
        data.append('contentType', 'text/markdown');
        data.append('content', content);
      }

      else if (contentType === 'image' && uploadedImage) {
        const ImageData = await ImageReader(uploadedImage)

        data.append('contentType', uploadedImage.type);
        data.append('content', ImageData);
        console.log(uploadedImage.type)

      }

      const response = await fetch(`${authorId}/posts/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrftoken,
          'Authorization': `Basic ${localStorage.getItem('authToken')}`,
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

  const ImageSelector = ({ images }) => {

    const [open, setOpen] = useState(false);
    const handleOpen = () => setOpen(true);
    const handleClose = () => setOpen(false);

    const [imageUrls, setImageUrls] = useState([]);

    useEffect(() => {
      const fetchImages = async () => {
        const fetchedUrls = await Promise.all(
          images.map(async (filename) => {
            const response = await fetch(filename, {
              headers: {
                'Authorization': `Basic ${localStorage.getItem('authToken')}`,
              },
            });
            const blob = await response.blob();
            return URL.createObjectURL(blob);
          })
        );

        setImageUrls(fetchedUrls);
      };

      fetchImages();
    }, []);

    function setImage(event) {
      setCommonmarkImage(event.target.id);
      handleClose();
    }

    return (
      <div>
        <button type="button" onClick={handleOpen} className='bg-customOrange rounded p-2 px-5'>Select Image</button>
        <Modal
          open={open}
          onClose={handleClose}
        >
          <Box sx={style}>
            <div className="grid grid-cols-2 pb-3 mb-3 border-b">
              <h2 className="font-bold text-3xl">
                Select Image
              </h2>
              <div className="flex justify-end">
                <CloseIcon sx={{ color: '#bbb' }} onClick={handleClose} className="cursor-pointer" />
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4">
              {
                imageUrls.length > 0 ? (
                  imageUrls.map((image, index) => {
                    return <img src={image} id={images[index].split("/").pop()} alt="Image not found" className='border rounded' onClick={setImage}></img>
                  })
                ) : (<p>No Images Found</p>)
              }
            </div>
          </Box>
        </Modal>
      </div>
    )
  }

  useEffect(() => {
    if (commonmarkImage) {
      let commonmarkImageText = `![Image](${window.location.origin}/media/images/${commonmarkImage})`
      setContent(content + commonmarkImageText);
      setCommonmarkImage('');
    }
  }, [commonmarkImage]);

  return (
    <div className="page max-h-screen overflow-scroll pb-[25px]">

      <form onSubmit={handleSubmit} className='form-make-post'>
        <h1 className='post-title'>Make a Post</h1>
        <div className='alldiv'>
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
            <label className='label-make-post' >Description:</label>
            <input
              type="text"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
              className='input-make-post'
            />

          </div>
          <div className='div-make-post'>
            <label> Content Type:</label>
          </div>

          <button
            className={`div-plain ${activeButton === 'plain' ? 'active' : ''}`} type="button"
            onClick={() => {
              setContentType('text/plain');
              setActiveButton('plain');
            }}>Plain Text </button>

          <button className={`div-markdown ${activeButton === 'markdown' ? 'active' : ''}`} type="button"
            onClick={() => {
              setContentType('text/markdown');
              setActiveButton('markdown');
            }}>MarkDown</button>

          <button className={`div-image ${activeButton === 'image' ? 'active' : ''}`} type="button"
            onClick={() => {
              setContentType('image');
              setActiveButton('image');
            }} x>Image</button>
          <br></br><br></br>

          <label>Content:</label>

          <div className='div-make-post'>

            {contentType === 'image' ? (
              <><input
                type="file"
                id="imageInput"
                onChange={(e) => setImage(e.target.files[0])}
                className="hidden"
              />

                <img
                  src="/upload.png"
                  alt="Upload"
                  className="w-10 h-10 cursor-pointer mx-auto hover:opacity-80"
                  onClick={() => document.getElementById('imageInput').click()}
                />  <p className="text-m text-gray-800 mt-2">
                  {uploadedImage ? uploadedImage.name : 'No file chosen'}
                </p></>) :
              (

                <textarea
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  required
                  className='make-post-textarea'

                />

              )}

          </div>

          <div className={`flex ${activeButton === "markdown" ? "justify-between" : "justify-end"} px-20 pb-8`}>
            {activeButton === "markdown" && <ImageSelector images={commonmarkImages} />}
            <select className='border rounded' value={visibility} onChange={handleChange}>
              <option value="PUBLIC">Public</option>
              <option value="FRIENDS">Friends-Only</option>
              <option value="UNLISTED">Unlisted</option>
            </select>
          </div>


          <div className="flex justify-end pr-20">
            <button type="submit" className="make-post-button">Create Post</button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default MakePost;
