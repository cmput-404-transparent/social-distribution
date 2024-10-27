import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import getCookie from '../getCSRFToken';
import Post from './post'; 

const SharePost = () => {
  const { author_id, post_id } = useParams();
  const [postData, setPostData] = useState(null);
  
  useEffect(() => {
    const fetchPost = async () => {
      console.log('Fetching post...');
      const csrftoken = getCookie('csrftoken');
    //   (`/api/authors/${author_id}/posts/${post_id}/`)
    try {
        const response = await fetch(`/api/authors/${author_id}/posts/${post_id}/`, {  
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken, 
            'Authorization': `Token ${localStorage.getItem('authToken')}`, 
          },
        });

        if (!response.ok) {
          const errorData = await response.json(); 
          throw new Error(`Error: ${errorData.detail}`);
        }
    
        const data = await response.json();
        console.log('Post retrieved successfully:', data);
        setPostData(data);
        
      } catch (err) {
        console.log("Error : " + err);
      } 
    };

    fetchPost();
  }, [author_id, post_id]);

  const handlePrompt = (e) => {
    e.preventDefault(); 
  };

  return (
    <div className = "page">
      
      {postData && <Post post={postData}  postState = {'ViewPost'} />} 
    </div>
  );
};

export default SharePost;
