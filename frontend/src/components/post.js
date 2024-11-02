import { useEffect, useState } from "react"
import getCookie from '../getCSRFToken';
import { marked } from 'marked';
import PeopleIcon from '@mui/icons-material/People';
import LinkIcon from '@mui/icons-material/Link';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import IconButton from '@mui/material/IconButton';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';
import FavoriteIcon from '@mui/icons-material/Favorite';

const PostState = {
  ViewPost: "ViewPost",
  ModifyPost: "ModifyPost"
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
              <div className="font-semibold text-xl font-mono">
                {post.title}
              </div>
              <div className="italic text-neutral-700 pb-3">
                {post.description}
              </div>
              <div className="text-m">
                {post.content}
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

export default function Post({ post }) {
  const [author, setAuthor] = useState("");
  const [self, setSelf] = useState({});
  const [isStream, setIsStream] = useState(false);
  const [isOwn, setIsOwn] = useState(false);

  const authorId = localStorage.getItem('authorId');
  const [postState, setPostState] = useState(PostState.ViewPost);

  const [likeNum, setLikeNum] = useState(0);
  const [selfLiked, setSelfLiked] = useState(false);

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
    <div className="grid auto-rows-auto grid-flow-row border-2 border-gray-400 rounded-md w-4/5 mx-auto relative px-12">
      <div className="grid grid-cols-[min-content,auto] auto-cols-auto border-b p-5">
        <div className="pr-8 min-w-[80px] min-h-[45px]">
          <img src="/pfp.png" alt="Profile" className="w-12 h-12 rounded-full object-cover" />
        </div>
        <div className="grid grid-flow-row auto-rows-auto space-y-4">
          <div className="grid grid-cols-[auto,min-content]">
            <a href={author.page} onClick={!isStream ? (e) => e.preventDefault() : null} className={`${!isStream ? "cursor-default" : "cursor-pointer"} flex items-center justify-start`}>
              <div className="flex justify-start items-center">
                <h1 className="font-bold text-lg font-sans">{post.author.displayName}</h1>
              </div>
            </a>
            <div className="text-right space-y">
              {(post.visibility !== "FRIENDS" || isOwn) && (
                <select id="Dropdown" onChange={dropdown} className="border rounded p-1 text-sm absolute top-3 right-3">
                  <option value="none">Options</option>
                  {!isStream && isOwn && <option value="edit">Edit</option>}
                  {!isStream && isOwn && <option value="delete">Delete</option>}
                  {post.visibility === "UNLISTED" && !isStream && isOwn && <option value="link">Copy Link</option>}
                  {post.visibility === "PUBLIC" && <option value="link">Share</option>}
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
      <Content post={post} postState={postState} />
      <div className="grid grid-cols-[min-content,min-content,auto] border-t px-2 space-x-3">
        <div className="flex items-center">
          <IconButton onClick={manageLike} className="!mr-[-2px]">
            {selfLiked ? <FavoriteIcon sx={{ color: '#dd0000' }} /> : <FavoriteBorderIcon />}
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
            {commentsNum !== 0 ? (
              <div className="border-b pb-4">
                <div className="space-y-3 overflow-y-scroll !max-h-[32rem]">
                  {comments.map((comment) => (
                    <Comment data={comment} />
                  ))}
                </div>
  
                {commentsNum !== comments.length && (
                  <div className="pt-3 flex justify-center">
                    <button className='bg-sky-400 rounded p-2 px-5' onClick={getMoreComments}>Load More</button>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex justify-center border-b pb-4">
                No comments yet
              </div>
            )}
  
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


