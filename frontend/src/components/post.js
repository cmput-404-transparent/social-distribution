import { useEffect, useState } from "react"
import getCookie from '../getCSRFToken';
import commonmark from 'commonmark';
import { marked } from 'marked';

const PostState = {
  ViewPost: "ViewPost",
  ModifyPost: "ModifyPost"
};

const Content = ({post, postState}) => {
  const [title, setTitle] = useState(post.title);
  const [description, setDescription] = useState(post.description);
  const [content, setContent] = useState(post.content);
  const [image, setImage] = useState('')

  useEffect(() => {

    setTitle(post.title);
    setDescription(post.description);
    if (post.contentType == 'text/plain'){
      setContent(post.content);
    }
    else if(post.contentType == 'text/markdown'){
      setContent(post.content);
    }
    
    else if (post.contentType == 'image'){
      setImage(post.content); 
      setContent(post.content);
    }
  }, [post])

  const ImageReader = (file) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      setImage(reader.result);
      setContent(reader.result); // If you want to set this as the content
    };
    reader.readAsDataURL(file); // Read the file as base64
  };

  const savePost = async function() {
    console.log("Saving post ");

    const updatedData = {
    title: title,
    description: description,
    content: content,
    };

    const csrftoken = getCookie('csrftoken');
    try{
      const response = await fetch(`/api/authors/${post.author}/posts/${post.id}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
          'Authorization': `Token ${localStorage.getItem('authToken')}`,
        },
        body: JSON.stringify(updatedData)
      });
      

    }
    catch(error){
      console.error('Error:', error);
    }
    window.location.reload(); 

  }

  if (post.contentType == 'text/plain') {
    return(
      <>
        {/* View Post section */}
        {postState == PostState.ViewPost &&
        <>
          <div className="p-5">
            <div className="font-bold text-2xl">
              {post.title}
            </div>
            <div className="italic text-neutral-700 pb-3">
              {post.description}
            </div>
            <div>
              {post.content}
            </div>
          </div>
        </>
        }
        
        {postState == PostState.ModifyPost &&
        <>
          <div className="p-5">
            <div className="font-bold text-2xl mb-4">
                <input type="text" value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
                />
            </div>
            <div className="italic text-neutral-700 mb-4">
              <input type="text" value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  required
                  />
            </div>
            <div className="mb-4">
              <input type="text" value={content}
                  onChange={(e) => setContent(e.target.value)}
                  required
                  />
            </div>

            <button
              onClick={savePost}
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            >Save</button>
          </div>
        </>
        }


      </>
      
    )
  }
  else if (post.contentType == 'text/markdown') {
    const postContentHTML = marked(post.content || '');
    return(
      <>
      {postState == PostState.ViewPost &&
        <>
      <div className="p-5">
        <div className="font-bold text-2xl">
          {post.title}
        </div>
        <div className="italic text-neutral-700 pb-3">
          {post.description}
        </div>
        <div>
        {/* Using dangerouslySetInnerHTML to render rich text into HTML 
        Reference- https://blog.logrocket.com/using-dangerouslysetinnerhtml-react-application/ */}
        <div dangerouslySetInnerHTML={{ __html: post.content }} className="post-content" />
        </div>
      </div>
      </>
    } 
      {postState == PostState.ModifyPost &&
          <>
            <div className="p-5">
              <div className="font-bold text-2xl mb-4">
                  <input type="text" value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                  />
              </div>
              <div className="italic text-neutral-700 mb-4">
                <input type="text" value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    required
                    />
              </div>
              <div className="mb-4">
                <input type="text" value={content}
                    onChange={(e) => setContent(e.target.value)}
                    required
                    />
              </div>

              <button
                onClick={savePost}
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              >Save</button>
            </div>
          </>
          }
    </>)
  }
  else if (post.contentType.includes('image')) {
    return(
      <>
      {postState == PostState.ViewPost &&
        <>
      <div className="p-5">
        <div className="font-bold text-2xl">
          {post.title}
        </div>
        <div className="italic text-neutral-700 pb-3">
          {post.description}
        </div>
        <div className="flex justify-center"><img src={post.content} className="w-1/2" /></div>
        
      </div>
      </>
    } 
    {postState == PostState.ModifyPost &&
          <>
            <div className="p-5">
              <div className="font-bold text-2xl mb-4">
                  <input type="text" value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                  />
              </div>
              <div className="italic text-neutral-700 mb-4">
                <input type="text" value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    required
                    />
              </div>
              <div className="mb-4">
              <input
              type="file"
              accept="image/*"
              onChange={(e) => ImageReader(e.target.files[0])}
              required
            />
                  
              </div>

              <button
                onClick={savePost}
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              >Save</button>
            </div>
          </>
          }
    </>)

      
    
  } 

}

export default function Post({ post }) {
  const [author, setAuthor] = useState("");
  const [isStream, setIsStream] = useState(false);
  const [postState, setPostState] = useState(PostState.ViewPost);
  
  useEffect(() => {
    fetch(`/api/authors/${post.author}/`)
    .then((r) => r.json())
    .then((data) => {
      setAuthor(data);
    });
    setIsStream(window.location.href.includes('stream'));
  }, []);

  const dropdown = (e) =>{
    const option = e.target.value
    if(option == "edit"){
      Edit()
    }
    else if(option == "delete"){
      Delete()
    }
  }
  
  const Edit = () =>{
    setPostState(PostState.ModifyPost);
    console.log('edit' + post.author)
  }

  const Delete = async() =>{
    const csrftoken = getCookie('csrftoken');
    try{
      const response = await fetch(`/api/authors/${post.author}/posts/${post.id}/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
          'Authorization': `Token ${localStorage.getItem('authToken')}`,
        }
      });
      
    }
    catch(error){
      console.error('Error:', error);
    }
    window.location.reload(); 
    
  }

  return(
    <>
      <div className="grid auto-rows-auto grid-flow-row border w-4/5 rounded relative">
        <a href={`/authors/${author.id}`}>
          <div className="grid grid-cols-[min-content,auto] auto-cols-auto border-b p-5">
            <div className="pr-8">
              profile picture
            </div>
            <div className="grid grid-flow-row auto-rows-auto space-y-4">
              <div>
                <h1 className="font-bold text-l">{author.display_name}</h1>
                <h2 className="text-l">@{author.username}</h2>
              </div>
              {
                !isStream && (
                  <select id = "Dropdown" onChange={dropdown} className="absolute top-2 right-2 border rounded p-1 text-sm">
                    <option>Options</option>
                    <option value="edit">Edit</option>
                    <option value="delete">Delete</option>
                  </select>
                )
              }
            </div>
          </div>
        </a>
        <Content post={post} postState={postState}/>
      </div>
    </>
  )
}

