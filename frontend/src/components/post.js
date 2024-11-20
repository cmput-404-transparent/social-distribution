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
import { PostProfilePicture } from "./profilePicture";


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

    const token = localStorage.getItem('authToken');

    const csrftoken = getCookie('csrftoken');
    try {
      await fetch(post.id + "/", {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
          'Authorization': `Basic ${localStorage.getItem('authToken')}`,
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
              <div className="font-semibold text-xl font-mono">
                {post.title}
              </div>
              <div>
              <div className="italic text-neutral-700 pb-3 post-description post-description" dangerouslySetInnerHTML={{ __html: post.description }}/> 
              </div>
              <div className="text-m">
              <div className="post-content" dangerouslySetInnerHTML={{ __html: post.content }} />
              </div>
            </div>
          </>
        }

        {postState === PostState.ModifyPost &&
          <>
            <div className="p-5">
              <div className="font-bold text-xl mb-4">
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
              <div>
              <div className="italic text-neutral-700 pb-3 post-description" dangerouslySetInnerHTML={{ __html: post.description }}/> 
              </div>
              <div>              
              
                {/* Using dangerouslySetInnerHTML to render rich text into HTML 
                  Reference- https://blog.logrocket.com/using-dangerouslysetinnerhtml-react-application/ */}
                <div className = "post-content" dangerouslySetInnerHTML={{ __html: postContentHTML }}  />
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
              <div className="italic text-neutral-700 pb-3 post-description post-description" dangerouslySetInnerHTML={{ __html: post.description }}/> 
              <div>
                 {/* eslint-disable-next-line */}
              <div className="flex justify-center post-content"><img src={post.content} className="w-1/2" alt="Image Not Found" /></div>
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

/**
 * source: ChatGPT (OpenAI)
 * prompt: "i have a time stamp like this in javascript "2024-11-01T21:50:39.064723Z" this is for a comment
 *          on a social media site i'm building. i want to get a string that says 'November11, 2024 at
 *          [time in current time zone]'"
 * date: November 1, 2024
 */
function formatDate(timestamp) {
  const date = new Date(timestamp);

  const formattedDate = new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'long',
    day: '2-digit',
    hour: 'numeric',
    minute: '2-digit',
    timeZoneName: 'short'
  }).format(date);

  return formattedDate;
}

const Comment = ({data}) => {
  return(
    <div className="border rounded p-4">
      <div className="grid grid-cols-[min-content,auto] space-x-4">
        <a href={data.author.page}>
          <PostProfilePicture displayName={data.author.displayName} imageURL={data.author.profileImage} />
        </a>
        <div className="grid grid-rows-[min-content,auto,auto]">
          <a href={data.author.page}><h1 className="font-bold text-l">{data.author.displayName}</h1></a>
          <p>{data.comment}</p>
          <p className="font-light italic text-sm pt-2">{formatDate(data.published)}</p>
        </div>
      </div>
    </div>
  )
}

/**
 * source: ChatGPT (OpenAI)
 * prompt: "i have a number that can be really big or small. i need it as a string. if
 *          number > 999 then i want it to be like 1.0k or 1.0m or 1.0b etc."
 * date: November 1, 2024
 */
function formatNumber(num) {
  if (Math.abs(num) >= 1.0e+9) {
    // Billions
    return (num / 1.0e+9).toFixed(1) + "b";
  } else if (Math.abs(num) >= 1.0e+6) {
    // Millions
    return (num / 1.0e+6).toFixed(1) + "m";
  } else if (Math.abs(num) >= 1.0e+3) {
    // Thousands
    return (num / 1.0e+3).toFixed(1) + "k";
  } else {
    // Less than 1,000, return the number as-is
    return num.toString();
  }
}

export default function Post({ post }) {
  const [author, setAuthor] = useState({});
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

  function getPostInfo() {
    fetch(post.id + "/", {
      headers: {
        'Authorization': `Basic ${localStorage.getItem('authToken')}`,
      },
    })
    .then(r => r.json())
    .then(data => {
      setAuthor(data.author);
      setLikeNum(data.likes.count);
      setComments(data.comments.src);
      setCommentsNum(data.comments.count);
    })
  }

  useEffect(() => {

    getPostInfo();

    fetch(`${post.author.id}/`, {
      headers: {
        'Authorization': `Basic ${localStorage.getItem('authToken')}`,
      },
    })
    .then(r => r.json())
    .then(data => {
      setSelf(data);
    })

    setIsStream(window.location.href.includes('stream'));

    setIsOwn(post.author.id === authorId);

    // eslint-disable-next-line
  }, []);

  useEffect(() => {
    if (Object.keys(self).length !== 0) {
      let postId = post.id.split("/").pop();
      fetch(`${self.id}` + "/liked/" + postId, {
        headers: {
          'Authorization': `Basic ${localStorage.getItem('authToken')}`,
        },
      })
      .then(r => r.json())
      .then(data => {
        setSelfLiked(data.liked);
      })
    }
  }, [author]);

  const sharePostURL = async (e) => {
    e.preventDefault();
    navigator.clipboard.writeText(post.page);
    alert("Link Copied!");
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
    const token = localStorage.getItem('authToken');
    try {
      await fetch(post.id + "/", {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
          'Authorization': `Basic ${token}`,
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
          'Authorization': `Basic ${localStorage.getItem('authToken')}`,
        },
      })
      .then(r => {
        getPostInfo();
      })
    }
  }

  const commentOnPost = async () => {
    const csrftoken = getCookie('csrftoken');

    const data = new URLSearchParams();
    data.append('comment', newComment);

    fetch(`${post.id}/comments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrftoken,
        'Authorization': `Basic ${localStorage.getItem('authToken')}`,
      },
      body: data.toString(),
    })
    .then(r => {
      if (r.ok) {
        setNewComment("");
        getPostInfo();
      }
    })
  }

  function getMoreComments() {
    let nextPageNum = (comments.length) % 5 + 2;
    fetch(`${post.id}/comments?page=${nextPageNum}`, {
      headers: {
        'Authorization': `Basic ${localStorage.getItem('authToken')}`,
      },
    })
    .then(r => r.json())
    .then(data => {
      setComments(comments.concat(data.src));
    })
  }

  return (
    <div className="grid auto-rows-auto grid-flow-row border rounded-md w-4/5 mx-auto relative">
      <div className="grid grid-cols-[min-content,auto] auto-cols-auto border-b p-4">
        <div className="mr-3 min-w-[80px] min-h-[45px]">
          <PostProfilePicture displayName={post.author.displayName} imageURL={post.author.profileImage} />
        </div>
        <div>
          <div className="grid grid-cols-[auto,min-content] h-full">
            <a href={post.author.page} onClick={!isStream ? (e) => e.preventDefault() : null} className={`${!isStream ? "cursor-default" : "cursor-pointer"} flex items-center justify-start`}>
              <div className="flex justify-start items-center">
                <h1 className="font-bold text-lg font-sans">{post.author.displayName}</h1>
              </div>
            </a>
            <div className={`text-right space-y ${post.visibility === "UNLISTED"? "grid grid-rows-2" : (post.visibility === "FRIENDS"? "flex items-center" : "")}`}>
              <div>
                {(post.visibility !== "FRIENDS" || isOwn) && (
                  <select id="Dropdown" onChange={dropdown} className="border rounded p-1 text-sm absolute top-3 right-3">
                    <option value="none">Options</option>
                    {!isStream && isOwn && <option value="edit">Edit</option>}
                    {!isStream && isOwn && <option value="delete">Delete</option>}
                    {(post.visibility === "PUBLIC" || post.visibility === "UNLISTED") && (
                        <option value="link">Copy Link</option>
                    )}
                  </select>
                )}
              </div>
              {post.visibility === "FRIENDS" ? (
                <div className="text-right text-neutral-400 whitespace-nowrap">
                  FRIENDS ONLY <PeopleIcon className="ml-1" />
                </div>
              ) : (
                post.visibility === "UNLISTED" && (
                  <div className="text-right text-neutral-400 whitespace-nowrap">
                    UNLISTED <LinkIcon className="ml-1" />
                  </div>
                )
              )}
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
                <FavoriteIcon sx={{ color: '#dd0000' }} />
              ) : (
                <FavoriteBorderIcon />
              )
            }
          </IconButton>
          {formatNumber(likeNum)}
        </div>
        <div className="flex items-center">
          <IconButton onClick={handleCommentsOpen}>
            <ChatBubbleOutlineIcon />
          </IconButton>
          {formatNumber(commentsNum)}
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
                  <div className="space-y-3 overflow-y-scroll !max-h-[32rem]">
                    {comments.map((comment) => (
                      <Comment data={comment} />
                    ))}
                  </div>

                  {
                    (commentsNum !== comments.length) && (
                      <div className="pt-3 flex justify-center">
                        <button className='bg-sky-400 rounded p-2 px-5' onClick={getMoreComments}>Load More</button>
                      </div>
                    )
                  }
                  
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
                <IconButton onClick={commentOnPost}>
                  <SendIcon />
                </IconButton>
              </div>
            </div>

          </Box>
        </Modal>
      </div>
    </div>
  );
}


