import { useEffect, useState } from "react"
import getCookie from '../getCSRFToken';
import { marked } from 'marked';
import PeopleIcon from '@mui/icons-material/People';
import LinkIcon from '@mui/icons-material/Link';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import IconButton from '@mui/material/IconButton';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';
import FavoriteIcon from '@mui/icons-material/Favorite';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import CloseIcon from '@mui/icons-material/Close';
import SendIcon from '@mui/icons-material/Send';


const PostState = {
  ViewPost: "ViewPost",
  ModifyPost: "ModifyPost"
};

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '40%',
  bgcolor: 'background.paper',
  borderRadius: "0.25rem",
  p: 4,
  maxHeight: '80%',
};

const Content = ({ post, postState }) => {
  const [title, setTitle] = useState(post.title);
  const [description, setDescription] = useState(post.description);
  const [content, setContent] = useState(post.content);
  const [image, setImage] = useState('')

  useEffect(() => {

    setTitle(post.title);
    setDescription(post.description);
    if (post.contentType === 'text/plain') {
      setContent(post.content);
    }
    else if (post.contentType === 'text/markdown') {
      setContent(post.content);
    }

    else if (post.contentType.includes('image')) {
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

  const savePost = async function () {
    console.log("Saving post ");

    const updatedData = {
      title: title,
      description: description,
      content: content,
    };

    const csrftoken = getCookie('csrftoken');
    try {
      await fetch(post.id + "/", {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
          'Authorization': `Token ${localStorage.getItem('authToken')}`,
        },
        body: JSON.stringify(updatedData)
      });
    }
    catch (error) {
      console.error('Error:', error);
    }
    window.location.reload();

  }

  const cancelEditPost = async function () {
    window.location.reload();
  }

  if (post.contentType === 'text/plain') {
    return (
      <>
        {/* View Post section */}
        {postState === PostState.ViewPost &&
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

        {postState === PostState.ModifyPost &&
          <>
            <div className="p-5">
              <div className="font-bold text-2xl mb-4">
                <input type="text" value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                  className="w-full"
                />
              </div>
              <div className="italic text-neutral-700 mb-4">
                <input type="text" value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  required
                  className="w-full"
                />
              </div>
              <div className="mb-4">
                <textarea type="text" value={content}
                  onChange={(e) => setContent(e.target.value)}
                  required
                  className="w-full"
                ></textarea>
              </div>

              <div className="space-x-3">
                <button
                  onClick={savePost}
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                >Save</button>

                <button
                  onClick={cancelEditPost}
                  className="bg-neutral-500 hover:bg-neutral-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                >Cancel</button>
              </div>
            </div>
          </>
        }
      </>
    )
  }
  else if (post.contentType === 'text/markdown') {
    const postContentHTML = marked(post.content || '');
    return (
      <>
        {postState === PostState.ViewPost &&
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
                <div dangerouslySetInnerHTML={{ __html: postContentHTML }} className="post-content" />
              </div>
            </div>
          </>
        }
        {postState === PostState.ModifyPost &&
          <>
            <div className="p-5">
              <div className="font-bold text-2xl mb-4">
                <input type="text" value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                  className="w-full"
                />
              </div>
              <div className="italic text-neutral-700 mb-4">
                <input type="text" value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  required
                  className="w-full"
                />
              </div>
              <div className="mb-4">
                <textarea type="text" value={content}
                  onChange={(e) => setContent(e.target.value)}
                  required
                  className="w-full"
                ></textarea>
              </div>

              <div className="space-x-3">
                <button
                  onClick={savePost}
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                >Save</button>

                <button
                  onClick={cancelEditPost}
                  className="bg-neutral-500 hover:bg-neutral-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                >Cancel</button>
              </div>
            </div>
          </>
        }
      </>)
  }
  else if (post.contentType.includes('image')) {
    return (
      <>
        {postState === PostState.ViewPost &&
          <>
            <div className="p-5">
              <div className="font-bold text-2xl">
                {post.title}
              </div>
              <div className="italic text-neutral-700 pb-3">
                {post.description}
              </div>
              {/* eslint-disable-next-line */}
              <div className="flex justify-center"><img src={post.content} className="w-1/2" alt="Image Not Found" /></div>

            </div>
          </>
        }
        {postState === PostState.ModifyPost &&
          <>
            <div className="p-5">
              <div className="font-bold text-2xl mb-4">
                <input type="text" value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                  className="w-full"
                />
              </div>
              <div className="italic text-neutral-700 mb-4">
                <input type="text" value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  required
                  className="w-full"
                />
              </div>
              <div className="mb-4">
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => ImageReader(e.target.files[0])}
                  required
                  className="w-full"
                />

              </div>

              <div className="space-x-3">
                <button
                  onClick={savePost}
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                >Save</button>

                <button
                  onClick={cancelEditPost}
                  className="bg-neutral-500 hover:bg-neutral-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                >Cancel</button>
              </div>
            </div>
          </>
        }
      </>)
  }
}

const Comment = ({data}) => {
  return(
    <div>

    </div>
  )
}

export default function Post({ post }) {
  const [author, setAuthor] = useState("");
  const [self, setSelf] = useState({});
  const [isStream, setIsStream] = useState(false);
  const [isOwn, setIsOwn] = useState(false);

  const authorId = localStorage.getItem('authorId');
  const [postState, setPostState] = useState(PostState.ViewPost);

  const [likeNum, setLikeNum] = useState(0);
  const [selfLiked, setSelfLiked] = useState(false);

  const [commentsOpen, setCommentsOpen] = useState(false);
  const handleCommentsOpen = () => setCommentsOpen(true);
  const handleCommentsClose = () => setCommentsOpen(false);

  const [commentsNum, setCommentsNum] = useState(0);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");

  useEffect(() => {
    fetch(post.author.id)
      .then((r) => r.json())
      .then((data) => {
        setAuthor(data);
      });

    let baseAuthorAPIUrl = post.author.id.split("/").slice(0, -1).join("/");
    fetch(`${baseAuthorAPIUrl}/${authorId}`)
    .then(r => r.json())
    .then(data => {
      setSelf(data);
    })

    setIsStream(window.location.href.includes('stream'));

    let postAuthorId = post.author.id.split("/").pop();

    setIsOwn(postAuthorId === authorId);

    fetch(`${post.id}/likes`)
    .then(r => r.json())
    .then(data => {
      setLikeNum(data.count);
    })

    // get comments for the post
    fetch(`${post.id}/comments`)
    .then(r => r.json())
    .then(data => {
      setComments(data.src);
      setCommentsNum(data.count);
    })

    // eslint-disable-next-line
  }, []);

  useEffect(() => {
    if (Object.keys(self).length !== 0) {
      let postId = post.id.split("/").pop();
      fetch(`${self.id}` + "/liked/" + postId)
      .then(r => r.json())
      .then(data => {
        setSelfLiked(data.liked);
      })
    }
  }, [author]);

  const sharePostURL = async (e) => {
    e.preventDefault();
    const authorId = author.id.split('/').pop(); 
    const postId = post.id.split('/').pop(); 
    const postUrl = `${window.location.origin}/authors/${authorId}/posts/${postId}`;    
    const title = "Link";
    const userResponse = window.prompt(title, postUrl);
    
    e.target.value = "none";
  };


  const dropdown = (e) => {
    const option = e.target.value
    if (option === "edit") {
      Edit()
    }
    else if (option === "delete") {
      Delete()
    }
    else if (option === "link") {
      sharePostURL(e)
    }
  }

  const Edit = () => {
    setPostState(PostState.ModifyPost);
    console.log('edit' + post.author)
  }

  const Delete = async () => {
    const csrftoken = getCookie('csrftoken');
    try {
      await fetch(post.id + "/", {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
          'Authorization': `Token ${localStorage.getItem('authToken')}`,
        }
      });

    }
    catch (error) {
      console.error('Error:', error);
    }
    window.location.reload();

  }

  const manageLike = async () => {
    let postId = post.id.split("/").pop();
    const csrftoken = getCookie('csrftoken');

    // can only like post that they haven't liked yet
    if (!selfLiked) {
      fetch(post.author.id + "/posts/" + postId + "/like", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrftoken,
        },
      })
      .then(r => {
        setSelfLiked(true);
        setLikeNum(likeNum + 1);
      })
    }
  }

  return (

    <div className="grid auto-rows-auto grid-flow-row border w-4/5 rounded relative">
      <div className="grid grid-cols-[min-content,auto] auto-cols-auto border-b p-5">
        <div className="pr-8">
          profile picture
        </div>
        <div className="grid grid-flow-row auto-rows-auto space-y-4">
          <div className="grid grid-cols-[auto,min-content]">
            <a href={`${author.page}`} onClick={!isStream ? (e) => { e.preventDefault() } : null} className={`${!isStream ? "cursor-default" : "cursor-pointer"} flex items-center-justify-start`} >
              <div className="flex justify-start items-center">
                <h1 className="font-bold text-l">{post.author.displayName}</h1>
              </div>
            </a>
            <div className={`grid grid-rows-${post.visibility !== "FRIENDS" || isOwn? "2" : "1"} text-right space-y`}>
              <div>
                {
                  (post.visibility !== "FRIENDS" || isOwn) && (
                    <select id="Dropdown" onChange={dropdown} className="border rounded p-1 text-sm absolute top-3 right-3">
                      <option value="none">Options</option>
                      {
                        !isStream && isOwn && (
                          <option value="edit">Edit</option>
                        )
                      }
                      {
                        !isStream && isOwn && (
                          <option value="delete">Delete</option>
                        )
                      }
                      {
                        post.visibility === "UNLISTED" && !isStream && isOwn && (
                          <option value="link">Copy Link</option>
                        )
                      }
                      {
                        post.visibility === "PUBLIC" && (
                          <option value="link">Share</option>
                        )
                      }
                    </select>
                  )
                }
              </div>

              {
                ((post.visibility === "FRIENDS") && (
                  <div className="text-right text-neutral-400 whitespace-nowrap">
                    FRIENDS ONLY <PeopleIcon className="ml-1" />
                  </div>
                )) ||
                ((post.visibility === "UNLISTED") && (
                  <div className="text-right text-neutral-400 whitespace-nowrap">
                    UNLISTED <LinkIcon className="ml-1" />
                  </div>
                ))
              }
            </div>

          </div>
        
        </div>
      </div>
      <Content post={post} postState={postState} />
      <div className="grid grid-cols-[min-content,min-content,auto] border-t px-2 space-x-3">
        <div className="flex items-center">
          <IconButton onClick={manageLike} className="!mr-[-2px]">
            {
              selfLiked? (
                <FavoriteIcon />
              ) : (
                <FavoriteBorderIcon />
              )
            }
          </IconButton>
          {likeNum}
        </div>
        <div className="flex items-center">
          <IconButton onClick={handleCommentsOpen}>
            <ChatBubbleOutlineIcon />
          </IconButton>
          {commentsNum}
        </div>

        <Modal
          open={commentsOpen}
          onClose={handleCommentsClose}
          aria-labelledby="modal-modal-title"
          aria-describedby="modal-modal-description"
        >
          <Box sx={style} className="space-y-4">
            <div className="grid grid-cols-2 border-b pb-4">
              <h2 className="font-bold text-3xl">
                {post.author.displayName}'s Post
              </h2>
              <div className="flex justify-end">
                <CloseIcon sx={{ color: '#bbb' }} onClick={handleCommentsClose} className="cursor-pointer" />
              </div>
            </div>

            {/* comments section */}
            {
              commentsNum !== 0? (
                <div className="border-b pb-4">
                  {comments.map((comment) => (
                    <Comment data={comment} />
                  ))}
                </div>
              ) : (
                <div className="flex justify-center border-b pb-4">
                  No comments yet
                </div>
              )
            }

            {/* create comment section */}
            <div>
              <div className="mb-4">
                <textarea type="text" value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                  placeholder="Write a comment..."
                  required
                  className="w-full border rounded p-2"
                ></textarea>
              </div>
              <div className="mt-[-20px] flex justify-end">
                <IconButton>
                  <SendIcon />
                </IconButton>
              </div>
            </div>

          </Box>
        </Modal>
      </div>
    </div>
  )
}

